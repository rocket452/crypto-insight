import asyncio
from cdp import CdpClient
import os
import json
from dotenv import load_dotenv

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
            return  # Exit if account creation fails
        
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
            print(f"   Liquidity available: {swap_price.liquidity_available}")
            
            # Check if min_to_amount exists
            if hasattr(swap_price, 'min_to_amount') and swap_price.min_to_amount:
                min_amount_weth = float(swap_price.min_to_amount) / 1e18
                print(f"   Min after slippage: {min_amount_weth:.6f} WETH")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: List all accounts
        print("\n=== TEST 3: List All Accounts ===")
        try:
            accounts_response = await cdp.evm.list_accounts()
            # Access the accounts from the response
            accounts_list = accounts_response.accounts if hasattr(accounts_response, 'accounts') else []
            print(f"✅ Found {len(accounts_list)} CDP accounts")
            for acc in accounts_list[:5]:  # Show first 5
                print(f"   - {acc.name}: {acc.address}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n🎉 All tests complete!")

if __name__ == "__main__":
    # Setup environment from JSON file
    if setup_environment():
        # Run the async test
        asyncio.run(test_cdp())
    else:
        print("❌ Failed to setup environment")
