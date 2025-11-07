import asyncio
from cdp import CdpClient
import os
from dotenv import load_dotenv

load_dotenv()

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
            print(f"   To: {swap_price.to_amount} WETH")
            print(f"   Min after slippage: {swap_price.min_to_amount} WETH")
            print(f"   Liquidity available: {swap_price.liquidity_available}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: List all accounts
        print("\n=== TEST 3: List All Accounts ===")
        try:
            accounts = await cdp.evm.list_accounts()
            print(f"✅ Found {len(accounts)} CDP accounts")
            for acc in accounts[:5]:  # Show first 5
                print(f"   - {acc.name}: {acc.address}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_cdp())
