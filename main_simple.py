# main_simple.py
import asyncio
from cdp import CdpClient
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Use the simple version (choose one):
from simple_llm import SimpleTradingLLM  # Tiny downloaded model
# from rule_based_ai import RuleBasedTradingAI  # OR: No download needed

# ... (keep your existing setup_environment function) ...

class SimpleTradingInsights:
    def __init__(self):
        self.technical_insights = []
        # Choose one of these:
        self.ai_advisor = SimpleTradingLLM()  # Small local model
        # self.ai_advisor = RuleBasedTradingAI()  # OR: Rule-based only
    
    def analyze_swap_opportunity(self, swap_data, from_token, to_token, from_amount):
        """Same technical analysis as before"""
        insights = []
        
        to_amount = float(swap_data.to_amount) / 1e18
        min_to_amount = float(swap_data.min_to_amount) / 1e18 if hasattr(swap_data, 'min_to_amount') and swap_data.min_to_amount else to_amount
        
        implied_price = to_amount / (float(from_amount) / 1e6)
        slippage = ((to_amount - min_to_amount) / to_amount * 100) if to_amount > 0 else 0
        
        if slippage < 0.5:
            insights.append(f"Excellent liquidity - {slippage:.2f}% slippage")
            liquidity_quality = "Excellent"
        elif slippage > 2.0:
            insights.append(f"High slippage: {slippage:.2f}% - caution needed")
            liquidity_quality = "Poor"
        else:
            insights.append(f"Moderate slippage: {slippage:.2f}%")
            liquidity_quality = "Good"
        
        insights.append(f"Swap rate: 1 {from_token} = {implied_price:.6f} {to_token}")
        
        return insights, {
            'slippage': slippage,
            'liquidity_quality': liquidity_quality,
            'swap_rate': f"1 {from_token} = {implied_price:.6f} {to_token}",
            'pair': f"{from_token}/{to_token}"
        }
    
    def get_ai_analysis(self, market_data: Dict, technical_insights: List) -> Dict:
        """Get AI analysis - now synchronous and simple"""
        return self.ai_advisor.analyze_trading_situation(market_data, technical_insights)

async def test_cdp_simple_ai():
    print("🤖 Testing CDP with SIMPLE Local AI\n")
    
    insights_engine = SimpleTradingInsights()
    
    async with CdpClient() as cdp:
        print("✅ CDP Client initialized\n")
        
        # Get account
        print("=== Getting Account ===")
        try:
            account = await cdp.evm.get_or_create_account(name="MyTestAccount")
            print(f"✅ Account: {account.address}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Test with AI insights
        print("\n=== Generating AI Trading Insights ===")
        try:
            USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
            WETH_BASE = "0x4200000000000000000000000000000000000006"
            from_amount = "1000000"  # 1 USDC
            
            print("🔄 Fetching swap data...")
            swap_data = await cdp.evm.get_swap_price(
                from_token=USDC_BASE,
                to_token=WETH_BASE,
                from_amount=from_amount,
                network="base",
                taker=account.address
            )
            
            # Get technical insights
            technical_insights, metrics = insights_engine.analyze_swap_opportunity(
                swap_data, "USDC", "WETH", from_amount
            )
            
            print("\n🔧 TECHNICAL ANALYSIS:")
            for insight in technical_insights:
                print(f"  • {insight}")
            
            # Get AI analysis (synchronous)
            print("\n🧠 AI TRADING ADVICE:")
            ai_analysis = insights_engine.get_ai_analysis(metrics, technical_insights)
            
            print(f"  Recommendation: {ai_analysis['recommendation']}")
            print(f"  Confidence: {ai_analysis['confidence']}")
            print(f"  Model: {ai_analysis['model']}")
            print(f"\n  Analysis: {ai_analysis['summary']}")
            
            if 'reasoning' in ai_analysis:
                print(f"  Reasoning: {ai_analysis['reasoning']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n🎉 Simple AI analysis complete!")

if __name__ == "__main__":
    if setup_environment():
        asyncio.run(test_cdp_simple_ai())
    else:
        print("❌ Failed to setup environment")
