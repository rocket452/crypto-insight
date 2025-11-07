from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv
import requests

# Get your current IP
current_ip = requests.get('https://api.ipify.org').text
print(f"🌐 Your current IPv4: {current_ip}")
print(f"   Add to allowlist: {current_ip}/32")

print("   testing IPv6")
try:
    ipv6 = requests.get('https://api64.ipify.org').text
    if ':' in ipv6:  # It's actually IPv6
        print(f"🌐 Your IPv6: {ipv6}")
        print(f"   Add to allowlist: {ipv6}/128")
except:
    print("   No IPv6 detected")

load_dotenv()

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

# Fix PEM format
if API_SECRET and '\\n' in API_SECRET:
    API_SECRET = API_SECRET.replace('\\n', '\n')

print(f"\n✅ API Key loaded: {API_KEY[:20]}...")
print(f"✅ Secret loaded (length: {len(API_SECRET) if API_SECRET else 0})")

try:
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    print("✅ Client initialized")
    
    print("\n=== TESTING CONNECTION ===")
    accounts = client.get_accounts()
    print("🎉 API connection successful!")
    
    print("\n=== ACCOUNT BALANCES ===")
    for account in accounts['accounts']:
        balance = float(account['available_balance']['value'])
        currency = account['available_balance']['currency']
        if balance > 0:
            print(f"💰 {currency}: {balance}")
            
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("1. Add your IP to allowlist at https://portal.cdp.coinbase.com")
    print("2. If you have IPv6, add that too")
    print("3. Wait 1-2 minutes after adding IP")
    print("4. Verify 'View' permission is enabled")
    print("5. Make sure you're using the correct portfolio/organization")
