import asyncio
from cdp import CdpClient
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Optional

# First, extract keys from JSON file and set them properly
def setup_environment():
    """Extract keys from cdp_api_key.json and set environment variables"""
    print("=== Setting up environment ===")
    
    # Check if JSON file exists
    json_path = 'cdp_api_key.json'
    if not os.path.exists(json_path):
        print(f"❌ {json_path} not found!")
        return False
    
    # Read and parse JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Extract values
    api_key_id = data.get('id')
    api_key_secret = data.get('privateKey', '')
    
    # Replace \n with actual newlines if needed
    if '\\n' in api_key_secret:
        api_key_secret = api_key_secret.replace('\\n', '\n')
    
    # Set environment variables with the correct names
    os.environ['CDP_API_KEY_ID'] = api_key_id
    os.environ['CDP_API_KEY_SECRET'] = api_key_secret
    
    # Get wallet secret from .env file
    load_dotenv()
    wallet_secret = os.getenv('CDP_WALLET_SECRET')
    
    if wallet_secret:
        os.environ['CDP_WALLET_SECRET'] = wallet_secret
        print(f"✅ CDP_WALLET_SECRET loaded")
    else:
        print("⚠️  CDP_WALLET_SECRET not found in .env")
        return False
    
    print(f"✅ CDP_API_KEY_ID: {api_key_id[:50]}...")
    print(f"✅ CDP_API_KEY_SECRET loaded (length: {len(api_key_secret)})")
    print()
    
    return True

class TradingInsights:
    def __init__(self):
        self.insights = []
    
    def analyze_swap_opportunity(self, swap_data, from_token, to_token, from_amount):
        """Analyze swap data to generate trading insights"""
        insights = []
        
        # Extract key metrics
        to_amount = float(swap_data.to_amount) / 1e18  # Convert from wei
        min_to_amount = float(swap_data.min_to_amount) / 1e18 if hasattr(swap_data, 'min_to_amount') and swap_data.min_to_amount else to_amount
        
        # Calculate implied price and slippage
        implied_price = to_amount / (float(from_amount) / 1e6)  # Assuming USDC has 6 decimals
        slippage = ((to_amount - min_to_amount) / to_amount * 100) if to_amount > 0 else 0
        
        # Generate insights based on the swap data
        if slippage < 0.5:
            insights.append({
                "type": "LOW_SLIPPAGE",
                "message": f"Excellent liquidity - only {slippage:.2f}% slippage",
                "confidence": "HIGH",
                "action": "FAVORABLE"
            })
        elif slippage > 2.0:
            insights.append({
                "type": "HIGH_SLIPPAGE",
                "message": f"High slippage warning: {slippage:.2f}% - consider smaller trade size",
                "confidence": "MEDIUM", 
                "action": "CAUTION"
            })
        else:
            insights.append({
                "type": "MODERATE_SLIPPAGE",
                "message": f"Moderate slippage: {slippage:.2f}% - acceptable for trading",
                "confidence": "MEDIUM",
                "action": "MONITOR"
            })
        
        # Price movement insights
        insights.append({
            "type": "PRICE_ANALYSIS",
            "message": f"Current swap rate: 1 USDC = {implied_price:.6f} WETH",
            "confidence": "HIGH",
            "action": "MONITOR"
        })
        
        # Liquidity insights
        if hasattr(swap_data, 'liquidity_available'):
            if swap_data.liquidity_available:
                insights.append({
                    "type": "LIQUIDITY",
                    "message": "High liquidity available for this swap",
                    "confidence": "HIGH",
                    "action": "FAVORABLE"
                })
        
        return insights
    
    def generate_market_sentiment(self, account_balance=None, recent_trades=None):
        """Generate broader market insights"""
        sentiment_insights = []
        
        # Basic market sentiment based on available data
        sentiment_insights.append({
            "type": "MARKET_OVERVIEW",
            "message": "Base network showing active DeFi activity",
            "confidence": "MEDIUM",
            "action": "RESEARCH"
        })
        
        # Time-based insights
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Market hours
            sentiment_insights.append({
                "type": "TRADING_HOURS",
                "message": "Currently in peak trading hours - higher volatility expected",
                "confidence": "HIGH",
                "action": "MONITOR"
            })
        
        # Account-specific insights
        if account_balance:
            sentiment_insights.append({
                "type": "PORTFOLIO_HEALTH",
                "message": "Account ready for trading operations",
                "confidence": "HIGH", 
                "action": "READY"
            })
        
        return sentiment_insights
    
    def generate_risk_assessment(self, swap_data, trade_size_usd=1.0):
        """Generate risk-related insights"""
        risk_insights = []
        
        # Basic risk assessment
        risk_insights.append({
            "type": "RISK_GENERAL",
            "message": "Always use stop-loss orders and position sizing",
            "confidence": "HIGH",
            "action": "CAUTION"
        })
        
        # Trade size risk (you can make this dynamic based on account balance)
        if trade_size_usd > 1000:
            risk_insights.append({
                "type": "POSITION_SIZE",
                "message": f"Large trade size (${trade_size_usd}) - consider splitting into smaller orders",
                "confidence": "MEDIUM",
                "action": "ADJUST"
            })
        
        return risk_insights
    
    def format_insights_for_display(self, insights):
        """Format insights for user-friendly display"""
        formatted = []
        
        for insight in insights:
            if insight["action"] in ["FAVORABLE", "READY"]:
                emoji = "🟢"
            elif insight["action"] in ["MONITOR", "RESEARCH"]:
                emoji = "🟡" 
            else:  # CAUTION, ADJUST
                emoji = "🔴"
                
            formatted.append(f"{emoji} [{insight['type']}] {insight['message']} (Confidence: {insight['confidence']})")
        
        return formatted

async def test_cdp_with_insights():
    print("=== Testing CDP Client with Trading Insights ===\n")
    
    # Initialize insights generator
    insights_engine = TradingInsights()
    
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
        
        # Test swap with insights
        print("\n=== Generating Trading Insights ===")
        try:
            # Define tokens (USDC to WETH on Base)
            USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
            WETH_BASE = "0x4200000000000000000000000000000000000006"
            from_amount = "1000000"  # 1 USDC
            
            # Get swap data
            swap_data = await cdp.evm.get_swap_price(
                from_token=USDC_BASE,
                to_token=WETH_BASE,
                from_amount=from_amount,
                network="base",
                taker=account.address
            )
            
            # Generate insights from swap data
            swap_insights = insights_engine.analyze_swap_opportunity(
                swap_data, "USDC", "WETH", from_amount
            )
            
            # Generate market sentiment
            market_insights = insights_engine.generate_market_sentiment(
                account_balance=True
            )
            
            # Generate risk assessment
            risk_insights = insights_engine.generate_risk_assessment(swap_data)
            
            # Combine all insights
            all_insights = swap_insights + market_insights + risk_insights
            
            # Display insights
            print("📊 TRADING INSIGHTS GENERATED:")
            print("-" * 50)
            
            formatted_insights = insights_engine.format_insights_for_display(all_insights)
            for insight in formatted_insights:
                print(f"  {insight}")
            
            # Show swap details
            to_amount_weth = float(swap_data.to_amount) / 1e18
            print(f"\n💱 Swap Details:")
            print(f"  1 USDC → {to_amount_weth:.6f} WETH")
            
            if hasattr(swap_data, 'min_to_amount') and swap_data.min_to_amount:
                min_amount_weth = float(swap_data.min_to_amount) / 1e18
                slippage = ((to_amount_weth - min_amount_weth) / to_amount_weth * 100) if to_amount_weth > 0 else 0
                print(f"  Max Slippage: {slippage:.2f}%")
            
        except Exception as e:
            print(f"❌ Error generating insights: {e}")
        
        # Enhanced account listing with insights
        print("\n=== Account Portfolio Analysis ===")
        try:
            accounts_response = await cdp.evm.list_accounts()
            accounts_list = accounts_response.accounts if hasattr(accounts_response, 'accounts') else []
            
            print(f"📈 Found {len(accounts_list)} trading accounts")
            
            # Generate portfolio insights
            portfolio_insights = [
                {
                    "type": "PORTFOLIO_DIVERSIFICATION",
                    "message": f"Manage {len(accounts_list)} trading accounts",
                    "confidence": "HIGH",
                    "action": "MONITOR"
                },
                {
                    "type": "RISK_MANAGEMENT", 
                    "message": "Consider separating strategies across accounts",
                    "confidence": "MEDIUM",
                    "action": "PLAN"
                }
            ]
            
            for insight in insights_engine.format_insights_for_display(portfolio_insights):
                print(f"  {insight}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

        print("\n🎉 Insight generation complete!")
        print("\n📊 Next Steps for Your App:")
        print("   1. Add historical price data for trend analysis")
        print("   2. Implement technical indicators (RSI, MACD)")
        print("   3. Add risk assessment scoring")
        print("   4. Create real-time alert system")

if __name__ == "__main__":
    if setup_environment():
        asyncio.run(test_cdp_with_insights())
    else:
        print("❌ Failed to setup environment")
