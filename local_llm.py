# local_llm.py
import requests
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime

class LocalTradingLLM:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        self.base_url = base_url
        self.model = model
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Define the expert trading persona for the LLM"""
        return """You are CryptoTrader-GPT, an expert quantitative trading analyst specializing in cryptocurrency markets. Your role is to analyze trading data and provide clear, actionable insights.

RESPONSE FORMAT:
- Market Assessment: Brief overview of current conditions
- Trading Recommendation: BUY/SELL/HOLD with specific reasoning
- Key Levels: Support and resistance levels to watch
- Risk Assessment: Potential risks and risk management advice
- Confidence Level: Low/Medium/High based on signal strength

Always be concise, professional, and focus on actionable insights. Use trading terminology appropriately."""

    async def analyze_trading_situation(self, market_data: Dict, technical_insights: List) -> Dict:
        """Analyze trading situation using local LLM"""
        
        user_prompt = self._build_trading_prompt(market_data, technical_insights)
        
        try:
            response = await self._call_ollama(user_prompt)
            parsed_response = self._parse_llm_response(response)
            return parsed_response
        except Exception as e:
            return self._get_fallback_response(str(e))

    def _build_trading_prompt(self, market_data: Dict, technical_insights: List) -> str:
        """Build comprehensive trading analysis prompt"""
        
        insights_text = "\n".join([f"• {insight}" for insight in technical_insights])
        
        prompt = f"""
TRADING ANALYSIS REQUEST

CURRENT MARKET DATA:
- Trading Pair: {market_data.get('pair', 'N/A')}
- Current Price: {market_data.get('current_price', 'N/A')}
- 24h Change: {market_data.get('price_change_24h', 'N/A')}
- Swap Rate: {market_data.get('swap_rate', 'N/A')}
- Slippage: {market_data.get('slippage', 'N/A')}%
- Liquidity: {market_data.get('liquidity_quality', 'N/A')}
- Volume: {market_data.get('volume_status', 'N/A')}

TECHNICAL INSIGHTS:
{insights_text}

MARKET CONTEXT:
- Network: Base
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
- Trade Size: {market_data.get('trade_size', 'Standard')}

Please analyze this trading situation and provide your expert assessment.
"""
        return prompt

    async def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama model"""
        
        # Use run_in_executor to avoid blocking the async loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            self._sync_ollama_call, 
            prompt
        )
        return response

    def _sync_ollama_call(self, prompt: str) -> str:
        """Synchronous call to Ollama (runs in thread pool)"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": self.system_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "num_predict": 500  # Limit response length
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30  # 30 second timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', 'No response generated')
            
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure it's running on localhost:11434"
        except requests.exceptions.Timeout:
            return "Error: Ollama request timed out. The model might be too slow."
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"

    def _parse_llm_response(self, response: str) -> Dict:
        """Parse the LLM response into structured data"""
        
        # Basic parsing - you can make this more sophisticated
        return {
            "raw_response": response,
            "summary": self._extract_summary(response),
            "recommendation": self._extract_recommendation(response),
            "confidence": self._extract_confidence(response),
            "key_levels": self._extract_key_levels(response),
            "risks": self._extract_risks(response),
            "timestamp": datetime.now().isoformat()
        }

    def _extract_summary(self, response: str) -> str:
        """Extract summary from response (first 2 sentences)"""
        sentences = response.split('. ')
        return '. '.join(sentences[:2]) + '.' if len(sentences) > 1 else response[:200] + "..."

    def _extract_recommendation(self, response: str) -> str:
        """Extract BUY/SELL/HOLD recommendation"""
        response_lower = response.lower()
        if 'buy' in response_lower and 'sell' not in response_lower:
            return "BUY"
        elif 'sell' in response_lower and 'buy' not in response_lower:
            return "SELL"
        else:
            return "HOLD"

    def _extract_confidence(self, response: str) -> str:
        """Extract confidence level"""
        response_lower = response.lower()
        if 'high confidence' in response_lower:
            return "HIGH"
        elif 'medium confidence' in response_lower:
            return "MEDIUM"
        elif 'low confidence' in response_lower:
            return "LOW"
        else:
            return "MEDIUM"  # Default

    def _extract_key_levels(self, response: str) -> List[str]:
        """Extract key price levels mentioned"""
        # Simple extraction - you can enhance this with regex
        levels = []
        words = response.split()
        for i, word in enumerate(words):
            if word in ['support', 'resistance', 'target', 'level'] and i + 1 < len(words):
                levels.append(f"{word}: {words[i+1]}")
        return levels[:3]  # Return first 3 levels

    def _extract_risks(self, response: str) -> List[str]:
        """Extract risk factors mentioned"""
        risks = []
        if 'risk' in response.lower():
            # Simple risk extraction
            sentences = response.split('. ')
            for sentence in sentences:
                if 'risk' in sentence.lower():
                    risks.append(sentence.strip())
        return risks[:2] or ["General market volatility"]

    def _get_fallback_response(self, error: str) -> Dict:
        """Provide fallback response when LLM fails"""
        return {
            "raw_response": f"LLM unavailable: {error}",
            "summary": "Using fallback analysis due to LLM unavailability.",
            "recommendation": "HOLD",
            "confidence": "LOW", 
            "key_levels": ["Monitor technical indicators manually"],
            "risks": ["System dependency risk - LLM service offline"],
            "timestamp": datetime.now().isoformat()
        }
