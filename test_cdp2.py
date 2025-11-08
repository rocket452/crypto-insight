import asyncio
from cdp import CdpClient
import os
import json
from dotenv import load_dotenv

def setup_environment():
    """Load all credentials from .env file"""
    print("=== Setting up environment ===")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get all values from .env
    api_key_id = os.getenv('CDP_API_KEY_ID')
    api_key_secret = os.getenv('CDP_API_KEY_SECRET')
    wallet_secret = os.getenv('CDP_WALLET_SECRET')
    
    if not all([api_key_id, api_key_secret, wallet_secret]):
        print("❌ Missing credentials in .env file")
        return False
    
    # Set environment variables
    os.environ['CDP_API_KEY_ID'] = api_key_id
    os.environ['CDP_API_KEY_SECRET'] = api_key_secret
    os.environ['CDP_WALLET_SECRET'] = wallet_secret
    
    print("✅ All credentials loaded from .env")
    return True

async def test_cdp():
    print("=== Testing CDP Client ===\n")
    
    # Create CDP client
    async with CdpClient() as cdp:
        print("✅ CDP Client initialized\n")
        
        # Test 1: Get or create an account
        print("=== TEST 1: Get or Create Account ===")
        try:
            account = await cdp.evm.get_or_create_account(name="MyTestAccount")
            print(f"✅ Account created/retrieved")
            print(f"   Name: {account.name}")
            print(f"   Address: {account.address}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Test 2: Get swap price (doesn't require funds)
        print("\n=== TEST 2: Get Swap Price ===")
        try:
            swap_price = await cdp.evm.get_swap_price(
                from_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
                to_token="0x4200000000000000000000000000000000000006",     # WETH on Base
                from_amount="1000000",  # 1 USDC (6 decimals)
                network="base",
                taker=account.address
            )
            
            print(f"✅ Swap price estimate:")
            print(f"   From: 1 USDC")
            # Convert from smallest unit (wei) to WETH
            to_amount_weth = float(swap_price.to_amount) / 1e18
            print(f"   To: {to_amount_weth:.6f} WETH")
            
            # Check various attributes that might exist
            if hasattr(swap_price, 'liquidity_available'):
                print(f"   Liquidity available: {swap_price.liquidity_available}")
            if hasattr(swap_price, 'min_to_amount') and swap_price.min_to_amount:
                min_amount_weth = float(swap_price.min_to_amount) / 1e18
                print(f"   Min after slippage: {min_amount_weth:.6f} WETH")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: List all accounts
        print("\n=== TEST 3: List All Accounts ===")
        try:
            accounts_response = await cdp.evm.list_accounts()
            accounts_list = accounts_response.accounts if hasattr(accounts_response, 'accounts') else []
            print(f"✅ Found {len(accounts_list)} CDP accounts")
            for acc in accounts_list[:5]:
                print(f"   - {acc.name}: {acc.address}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n🎉 All tests complete! Your CDP connection is working!")
        print("\n📌 Next steps:")
        print("   1. Fund your account with USDC on Base")
        print("   2. Execute actual swaps")
        print("   3. Integrate with your crypto analysis tool")

if __name__ == "__main__":
    if setup_environment():
        asyncio.run(test_cdp())
    else:
        print("❌ Failed to setup environment")
