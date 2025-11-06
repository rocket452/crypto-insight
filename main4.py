from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

print("=== API KEY DIAGNOSTICS ===")
print(f"API Key: {API_KEY}")
print(f"Secret starts with: {API_SECRET[:50]}")
print(f"Secret ends with: {API_SECRET[-50:]}")
print(f"Secret contains BEGIN: {'BEGIN' in API_SECRET}")
print(f"Secret contains END: {'END' in API_SECRET}")

# Check if it's a multi-line PEM in .env file
if '\\n' in API_SECRET:
    print("⚠️  Found \\n in secret - might need proper newlines")
else:
    print("✅ No \\n found in secret")

try:
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    print("✅ Client initialized")
    
    # Try a simple public endpoint first
    print("\n=== TESTING PUBLIC ENDPOINT ===")
    from coinbase.rest import RESTClient
    public_client = RESTClient()  # No auth for public endpoints
    currencies = public_client.get_currencies()
    print("✅ Public API works - network connectivity is good")
    
    # Now test authenticated endpoint
    print("\n=== TESTING AUTHENTICATED ENDPOINT ===")
    accounts = client.get_accounts()
    print("✅ Authenticated API call successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    if "401" in str(e):
        print("\n🔍 401 Unauthorized - Common Solutions:")
        print("1. Check API key PERMISSIONS in Coinbase Cloud")
        print("2. Ensure key has 'View' permission enabled")
        print("3. Verify organization/portfolio selection")
        print("4. Check if key is activated (new keys may take 1-2 minutes)")
