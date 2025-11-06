from coinbase.rest import RESTClient
import json
import os

# Debug: Check if environment variables are loaded
print("=== CHECKING ENVIRONMENT VARIABLES ===")
API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

print(f"API Key retrieved: {'✅ SUCCESS' if API_KEY else '❌ FAILED'}")
print(f"API Secret retrieved: {'✅ SUCCESS' if API_SECRET else '❌ FAILED'}")

if not API_KEY or not API_SECRET:
    print("❌ ERROR: Missing API credentials. Please check your environment variables.")
    exit(1)

# Check key format (partial for security)
if API_KEY:
    print(f"API Key starts with: {API_KEY[:8]}...")
if API_SECRET:
    print(f"API Secret starts with: {API_SECRET[:8]}...")

print("\n=== INITIALIZING CLIENT ===")
try:
    # Initialize client
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    print("✅ Client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    exit(1)

print("\n=== TESTING API CONNECTION ===")
try:
    # Get account balances
    accounts = client.get_accounts()
    print("✅ API connection successful")
    print(f"✅ Received response with {len(accounts.get('accounts', []))} accounts")
    
except Exception as e:
    print(f"❌ API call failed: {e}")
    print("This could be due to:")
    print("  - Invalid API credentials")
    print("  - Network connectivity issues")
    print("  - Exchange API downtime")
    exit(1)

print("\n=== ACCOUNT BALANCES ===")
try:
    # Print all balances
    non_zero_accounts = 0
    total_balance = 0
    
    for account in accounts['accounts']:
        balance = float(account['available_balance']['value'])
        if balance > 0:
            currency = account['available_balance']['currency']
            print(f"✅ {currency}: {balance}")
            non_zero_accounts += 1
            total_balance += balance
    
    print(f"\n📊 Summary: Found {non_zero_accounts} accounts with non-zero balances")
    print(f"💰 Total balance across all currencies: {total_balance}")
    
    if non_zero_accounts == 0:
        print("💡 Note: All accounts show zero balance. This is normal if you haven't funded your account yet.")

except Exception as e:
    print(f"❌ Error processing balances: {e}")

print("\n=== SPECIFIC CURRENCY CHECK ===")
# Get specific currency balance
def get_balance(currency='BTC'):
    try:
        accounts = client.get_accounts()
        for account in accounts['accounts']:
            if account['available_balance']['currency'] == currency:
                return float(account['available_balance']['value'])
        return 0
    except Exception as e:
        print(f"❌ Error getting {currency} balance: {e}")
        return -1

# Check multiple common currencies
common_currencies = ['BTC', 'ETH', 'USD', 'USDC', 'LTC']

for currency in common_currencies:
    balance = get_balance(currency)
    if balance > 0:
        print(f"✅ {currency} Balance: {balance}")
    elif balance == 0:
        print(f"💡 {currency} Balance: 0 (not held)")
    else:
        print(f"❌ Could not retrieve {currency} balance")

print("\n=== CONNECTION TEST COMPLETE ===")
print("✅ Script completed successfully if no errors above")
