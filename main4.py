from coinbase.rest import RESTClient
import json
import os
from dotenv import load_dotenv  # Add this import

print("=== LOADING ENVIRONMENT VARIABLES ===")

# Load environment variables from .env file
load_dotenv()  # Add this line - it loads the .env file

# Now check if .env file was found
env_path = '.env'
if os.path.exists(env_path):
    print(f"✅ .env file found at: {os.path.abspath(env_path)}")
else:
    print(f"❌ .env file NOT found at: {os.path.abspath(env_path)}")
    print("Please make sure your .env file is in the same directory as your script")

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

print(f"API Key retrieved: {'✅ SUCCESS' if API_KEY else '❌ FAILED'}")
print(f"API Secret retrieved: {'✅ SUCCESS' if API_SECRET else '❌ FAILED'}")

# Debug: Print all environment variables (be careful with this in shared environments)
print("\n=== CHECKING ALL ENV VARIABLES ===")
all_env_vars = os.environ
for key, value in all_env_vars.items():
    if 'API' in key or 'KEY' in key or 'SECRET' in key:
        print(f"Found env var: {key} = {value[:8]}...")  # Only show first 8 chars for security

if not API_KEY or not API_SECRET:
    print("\n❌ ERROR: Missing API credentials.")
    print("Possible solutions:")
    print("1. Make sure your .env file is in the same directory as your script")
    print("2. Check that variable names in .env match exactly: CDP_API_KEY_ID and CDP_API_KEY_SECRET")
    print("3. Ensure .env file format is correct (no spaces around =)")
    exit(1)

print("\n=== .ENV FILE FORMAT EXAMPLE ===")
print("Your .env file should look like this:")
print("CDP_API_KEY_ID=your_actual_key_here")
print("CDP_API_KEY_SECRET=your_actual_secret_here")
print("(No quotes, no spaces around the = sign)")

# Rest of your code continues...
print("\n=== INITIALIZING CLIENT ===")
try:
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    print("✅ Client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    exit(1)

print("\n=== TESTING API CONNECTION ===")
try:
    accounts = client.get_accounts()
    print("✅ API connection successful")
    print(f"✅ Received response with {len(accounts.get('accounts', []))} accounts")
    
except Exception as e:
    print(f"❌ API call failed: {e}")
    exit(1)

print("\n=== ACCOUNT BALANCES ===")
# Print all balances
for account in accounts['accounts']:
    balance = float(account['available_balance']['value'])
    if balance > 0:
        currency = account['available_balance']['currency']
        print(f"✅ {currency}: {balance}")

print("\n=== SCRIPT COMPLETE ===")
