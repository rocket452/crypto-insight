from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv
import json

import requests
current_ip = requests.get('https://api.ipify.org').text
print(f"Add this IP to your allowlist: {current_ip}/32")

load_dotenv()

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

print("=== FIXING PEM FORMAT ===")
# Replace \n with actual newlines
if '\\n' in API_SECRET:
    print("Converting \\n to actual newlines...")
    API_SECRET = API_SECRET.replace('\\n', '\n')
    print("✅ Fixed PEM format")

print(f"Secret preview:\n{API_SECRET[:100]}...")

try:
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    print("✅ Client initialized with fixed PEM")
    
    # Test the connection
    print("\n=== TESTING CONNECTION ===")
    accounts = client.get_accounts()
    print("✅ API connection successful!")
    print(f"Found {len(accounts['accounts'])} accounts")
    
    # Show balances
    print("\n=== ACCOUNT BALANCES ===")
    for account in accounts['accounts']:
        balance = float(account['available_balance']['value'])
        currency = account['available_balance']['currency']
        if balance > 0:
            print(f"💰 {currency}: {balance}")
        else:
            print(f"💡 {currency}: 0")
            
except Exception as e:
    print(f"❌ Error: {e}")
    
    # Additional debug info
    if "401" in str(e):
        print("\n🔍 Still getting 401 - Let's check:")
        print("1. Go to https://cloud.coinbase.com/access/api")
        print("2. Verify your API key has 'View' permissions")
        print("3. Check IP allowlist includes your current IP")
        print("4. Ensure you selected the correct organization/portfolio")
