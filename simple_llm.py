# simple_llm.py
from transformers import pipeline, set_seed
import torch
from typing import Dict, List
import re
import random

class SimpleTradingLLM:
    def __init__(self):
        # Use a better model for analysis - Facebook's BART is good for summarization/analysis
        self.model_name = "facebook/bart-large-mnli"  # Better for analysis tasks
        # Alternative: "microsoft/DialoGPT-medium" for conversation
        # Alternative: "gpt2" for general text generation
        
        print("🔄 Loading local AI model (this may take a minute first time)...")
        try:
            # Use text generation with a model that's good at analysis
            self.generator = pipeline(
                "text-generation",
                model="gpt2",  # Let's try GPT-2 instead, it's more reliable
                torch_dtype=torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
            )
            set_seed(42)  # For reproducible results
            print("✅ Local AI model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.generator = None
    
    def analyze_trading_situation(self, market_data: Dict, technical_insights: List) -> Dict:
        """Simple analysis without complex setup"""
        
        if not self.generator:
            return self._get_fallback_analysis()
        
        prompt = self._build_structured_prompt(market_data, technical_insights)
        
        try:
            # Generate response with better parameters
            response = self.generator(
                prompt,
                max_new_tokens=150,  # Use max_new_tokens instead of max_length
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                truncation=True,  # Explicitly enable truncation
                pad_token_id=50256,
                no_repeat_ngram_size=2  # Avoid repeating phrases
            )
            
            llm_text = response[0]['generated_text']
            return self._parse_enhanced_response(llm_text, prompt)
            
        except Exception as e:
            print(f"⚠️  AI model error: {e}")
            return self._get_enhanced_fallback_analysis(market_data)
    
    def _build_structured_prompt(self, market_data: Dict, technical_insights: List) -> str:
        """Build a more structured prompt for better responses"""
        
        insights_text = "\n".join([f"- {insight}" for insight in technical_insights])
        slippage = market_data.get('slippage', 0)
        liquidity = market_data.get('liquidity_quality', 'Unknown')
        
        prompt = f"""
Trading Analysis Request:

CURRENT MARKET CONDITIONS:
- Trading Pair: {market_data.get('pair', 'USDC/WETH')}
- Swap Rate: {market_data.get('swap_rate', 'N/A')}
- Slippage: {slippage:.2f}%
- Liquidity Quality: {liquidity}

TECHNICAL OBSERVATIONS:
{insights_text}

ANALYSIS REQUEST:
Based on the above data, provide a brief crypto trading analysis with:
1. Overall assessment of the trading opportunity
2. Clear recommendation: BUY, SELL, or HOLD
3. Key factors influencing this decision
4. Risk level: LOW, MEDIUM, or HIGH

Analysis:
"""
        return prompt.strip()
    
    def _parse_enhanced_response(self, response: str, original_prompt: str) -> Dict:
        """Better parsing of the response"""
        
        # Remove the original prompt from response
        clean_response = response.replace(original_prompt, "").strip()
        
        # If response is too short or generic, enhance it
        if len(clean_response) < 20 or "what should i do" in clean_response.lower():
            return self._get_enhanced_fallback_analysis({})
        
        # Extract recommendation with better logic
        recommendation = "HOLD"
        response_upper = clean_response.upper()
        
        if "BUY" in response_upper and "SELL" not in response_upper:
            recommendation = "BUY"
        elif "SELL" in response_upper and "BUY" not in response_upper:
            recommendation = "SELL"
        elif "HOLD" in response_upper:
            recommendation = "HOLD"
        else:
            # If no clear recommendation, analyze sentiment
            positive_words = ['good', 'strong', 'favorable', 'excellent', 'positive', 'bullish']
            negative_words = ['poor', 'weak', 'unfavorable', 'caution', 'negative', 'bearish']
            
            positive_count = sum(1 for word in positive_words if word in clean_response.lower())
            negative_count = sum(1 for word in negative_words if word in clean_response.lower())
            
            if positive_count > negative_count:
                recommendation = "BUY"
            elif negative_count > positive_count:
                recommendation = "SELL"
        
        # Extract confidence
        confidence = "MEDIUM"
        if "HIGH" in response_upper or "STRONG" in response_upper or "EXCELLENT" in response_upper:
            confidence = "HIGH"
        elif "LOW" in response_upper or "WEAK" in response_upper or "POOR" in response_upper:
            confidence = "LOW"
        
        # Create a better summary
        sentences = re.split(r'[.!?]+', clean_response)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        summary = ". ".join(meaningful_sentences[:2]) + "." if meaningful_sentences else clean_response[:150] + "..."
        
        return {
            "raw_response": clean_response,
            "recommendation": recommendation,
            "confidence": confidence,
            "summary": summary,
            "model": "gpt2"
        }
    
    def _get_enhanced_fallback_analysis(self, market_data: Dict) -> Dict:
        """Better fallback when model isn't available or gives poor response"""
        
        slippage = market_data.get('slippage', 0)
        liquidity = market_data.get('liquidity_quality', 'Unknown')
        
        # Rule-based fallback
        if slippage < 0.5 and liquidity == 'Excellent':
            recommendation = "BUY"
            confidence = "HIGH"
            analysis = f"Excellent trading conditions with low slippage ({slippage:.2f}%) and strong liquidity. Favorable for execution."
        elif slippage > 2.0:
            recommendation = "SELL"
            confidence = "MEDIUM"
            analysis = f"High slippage ({slippage:.2f}%) suggests poor liquidity. Consider waiting for better conditions or using limit orders."
        else:
            recommendation = "HOLD"
            confidence = "MEDIUM"
            analysis = f"Moderate market conditions with {slippage:.2f}% slippage. Monitor for better entry points."
        
        return {
            "raw_response": analysis,
            "recommendation": recommendation,
            "confidence": confidence,
            "summary": analysis,
            "model": "rule-based-fallback"
        }
