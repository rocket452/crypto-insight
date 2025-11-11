# simple_llm.py
from transformers import pipeline
import torch
from typing import Dict, List
import re

class SimpleTradingLLM:
    def __init__(self):
        # Use a tiny, fast model that doesn't require much RAM
        self.model_name = "microsoft/DialoGPT-small"  # Only 300MB!
        # Alternative: "distilgpt2" (even smaller)
        
        print("🔄 Loading local AI model (this may take a minute first time)...")
        try:
            # Use a simple text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model_name,
                torch_dtype=torch.float32,  # Use float32 to save memory
                device_map="auto" if torch.cuda.is_available() else None,
            )
            print("✅ Local AI model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.generator = None
    
    def analyze_trading_situation(self, market_data: Dict, technical_insights: List) -> Dict:
        """Simple analysis without complex setup"""
        
        if not self.generator:
            return self._get_fallback_analysis()
        
        prompt = self._build_simple_prompt(market_data, technical_insights)
        
        try:
            # Generate response (keep it short)
            response = self.generator(
                prompt,
                max_length=400,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256  # GPT2 pad token
            )
            
            llm_text = response[0]['generated_text']
            return self._parse_simple_response(llm_text, prompt)
            
        except Exception as e:
            print(f"⚠️  AI model error: {e}")
            return self._get_fallback_analysis()
    
    def _build_simple_prompt(self, market_data: Dict, technical_insights: List) -> str:
        """Build a very simple prompt"""
        
        insights_text = " | ".join(technical_insights)
        
        prompt = f"""
As a crypto trading assistant, analyze this swap opportunity:

Trading: {market_data.get('pair', 'USDC/WETH')}
Swap Rate: {market_data.get('swap_rate', 'N/A')}
Slippage: {market_data.get('slippage', 'N/A')}%
Liquidity: {market_data.get('liquidity_quality', 'N/A')}

Technical Insights: {insights_text}

Should I execute this trade? Provide brief analysis with BUY/SELL/HOLD recommendation.
"""
        return prompt.strip()
    
    def _parse_simple_response(self, response: str, original_prompt: str) -> Dict:
        """Simple parsing of the response"""
        
        # Remove the original prompt from response
        clean_response = response.replace(original_prompt, "").strip()
        
        # Extract recommendation
        recommendation = "HOLD"
        if "BUY" in response.upper():
            recommendation = "BUY"
        elif "SELL" in response.upper():
            recommendation = "SELL"
        
        # Extract confidence (simple heuristic)
        confidence = "MEDIUM"
        if "HIGH" in response.upper() or "STRONG" in response.upper():
            confidence = "HIGH"
        elif "LOW" in response.upper() or "WEAK" in response.upper():
            confidence = "LOW"
        
        return {
            "raw_response": clean_response,
            "recommendation": recommendation,
            "confidence": confidence,
            "summary": clean_response[:200] + "..." if len(clean_response) > 200 else clean_response,
            "model": self.model_name
        }
    
    def _get_fallback_analysis(self) -> Dict:
        """Fallback when model isn't available"""
        return {
            "raw_response": "AI analysis unavailable. Using rule-based assessment.",
            "recommendation": "HOLD",
            "confidence": "LOW",
            "summary": "Check technical insights above for manual decision.",
            "model": "fallback"
        }
