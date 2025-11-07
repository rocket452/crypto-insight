from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

if API_SECRET and '\\n' in API_SECRET:
    API_SECRET = API_SECRET.replace('\\n', '\n')

try:
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    print("✅ Client initialized\n")
    
    # Get your trading account balances
    print("=== YOUR COINBASE TRADING BALANCES ===")
    
    # List your actual Coinbase accounts (not CDP wallets)
    try:
        # This should show your actual Coinbase balances
        accounts = client.get_accounts()
        
        if 'accounts' in accounts:
            print(f"Found {len(accounts['accounts'])} accounts:\n")
            for account in accounts['accounts']:
                balance = float(account.get('available_balance', {}).get('value', 0))
                currency = account.get('currency', 'UNKNOWN')
                if balance > 0:
                    print(f"💰 {currency}: {balance}")
                else:
                    print(f"💡 {currency}: 0")
        else:
            print("No accounts found")
            print(f"Response: {accounts}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📌 This API key is for CDP, not regular Coinbase trading")
        print("   You might need to use the Coinbase Exchange API instead")
        
except Exception as e:
    print(f"❌ Connection error: {e}")
