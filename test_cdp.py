# main.py
import asyncio
from cdp import CdpClient
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from local_llm import LocalTradingLLM  # Import our local LLM

# ... (keep your existing setup_environment function) ...

class EnhancedTradingInsights:
    def __init__(self):
        self.technical_insights = []
        self.llm_advisor = LocalTradingLLM(model="mistral")  # Use local model
    
    def analyze_swap_opportunity(self, swap_data, from_token, to_token, from_amount):
        """Enhanced analysis with more metrics for LLM"""
        insights = []
        
        # Extract key metrics
        to_amount = float(swap_data.to_amount) / 1e18
        min_to_amount = float(swap_data.min_to_amount) / 1e18 if hasattr(swap_data, 'min_to_amount') and swap_data.min_to_amount else to_amount
        
        # Calculate metrics
        implied_price = to_amount / (float(from_amount) / 1e6)
        slippage = ((to_amount - min_to_amount) / to_amount * 100) if to_amount > 0 else 0
        
        # Generate detailed insights for LLM
        if slippage < 0.5:
            insights.append(f"Excellent liquidity conditions with only {slippage:.2f}% slippage")
            liquidity_quality = "Excellent"
        elif slippage > 2.0:
            insights.append(f"High slippage warning: {slippage:.2f}% - consider smaller orders")
            liquidity_quality = "Poor"
        else:
            insights.append(f"Moderate slippage: {slippage:.2f}% - acceptable for trading")
            liquidity_quality = "Good"
        
        insights.append(f"Current swap rate: 1 {from_token} = {implied_price:.6f} {to_token}")
        
        # Volume assessment (simulated - you'd get real volume data)
        volume_status = "High" if slippage < 1.0 else "Moderate"
        insights.append(f"Market depth appears {volume_status.lower()}")
        
        return insights, {
            "slippage": slippage,
            "liquidity_quality": liquidity_quality,
            "volume_status": volume_status,
            "swap_rate": f"1 {from_token} = {implied_price:.6f} {to_token}"
        }
    
    async def get_comprehensive_analysis(self, swap_data, from_token, to_token, from_amount):
        """Get both technical and LLM analysis"""
        
        # Get technical insights
        technical_insights, metrics = self.analyze_swap_opportunity(
            swap_data, from_token, to_token, from_amount
        )
        
        # Prepare market data for LLM
        market_data = {
            "pair": f"{from_token}/{to_token}",
            "current_price": "N/A",  # You would get this from price feeds
            "price_change_24h": "N/A", 
            "swap_rate": metrics["swap_rate"],
            "slippage": metrics["slippage"],
            "liquidity_quality": metrics["liquidity_quality"],
            "volume_status": metrics["volume_status"],
            "trade_size": f"{float(from_amount) / 1e6} {from_token}"
        }
        
        # Get LLM analysis
        llm_analysis = await self.llm_advisor.analyze_trading_situation(
            market_data, technical_insights
        )
        
        return {
            "technical_insights": technical_insights,
            "metrics": metrics,
            "llm_analysis": llm_analysis,
            "timestamp": datetime.now().isoformat()
        }

async def test_cdp_with_local_llm():
    print("🤖 Testing CDP Client with LOCAL LLM Insights\n")
    
    # Initialize enhanced insights generator
    insights_engine = EnhancedTradingInsights()
    
    async with CdpClient() as cdp:
        print("✅ CDP Client initialized\n")
        
        # Get or create account
        print("=== Getting Account ===")
        try:
            account = await cdp.evm.get_or_create_account(name="MyTestAccount")
            print(f"✅ Account: {account.address}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Test swap with local LLM insights
        print("\n=== Generating Local LLM Trading Insights ===")
        try:
            # Define tokens
            USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
            WETH_BASE = "0x4200000000000000000000000000000000000006"
            from_amount = "1000000"  # 1 USDC
            
            print("🔄 Fetching swap data from CDP...")
            swap_data = await cdp.evm.get_swap_price(
                from_token=USDC_BASE,
                to_token=WETH_BASE,
                from_amount=from_amount,
                network="base",
                taker=account.address
            )
            
            print("🧠 Analyzing with local LLM...")
            analysis = await insights_engine.get_comprehensive_analysis(
                swap_data, "USDC", "WETH", from_amount
            )
            
            # Display results
            print("\n" + "="*60)
            print("📊 TRADING ANALYSIS REPORT")
            print("="*60)
            
            print("\n🔧 TECHNICAL INSIGHTS:")
            for insight in analysis["technical_insights"]:
                print(f"  • {insight}")
            
            print(f"\n🤖 LOCAL LLM ANALYSIS (using {insights_engine.llm_advisor.model}):")
            llm = analysis["llm_analysis"]
            print(f"  Recommendation: {llm['recommendation']}")
            print(f"  Confidence: {llm['confidence']}")
            print(f"\n  Summary: {llm['summary']}")
            
            if llm['key_levels']:
                print(f"\n  Key Levels:")
                for level in llm['key_levels']:
                    print(f"    • {level}")
            
            if llm['risks']:
                print(f"\n  Risks:")
                for risk in llm['risks']:
                    print(f"    • {risk}")
            
            # Show raw LLM response for debugging
            print(f"\n  Raw LLM Response:")
            print(f"    {llm['raw_response'][:300]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n🎉 Local LLM analysis complete!")
        print("\n💡 Next: Add price feeds and historical data for better analysis")

if __name__ == "__main__":
    if setup_environment():
        asyncio.run(test_cdp_with_local_llm())
    else:
        print("❌ Failed to setup environment")
