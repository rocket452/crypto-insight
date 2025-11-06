from coinbase.rest import RESTClient
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

print("Key format check:")
print(f"API Key: {API_KEY[:20]}...")
print(f"Secret starts with: {API_SECRET[:50]}")

if "BEGIN EC PRIVATE KEY" in API_SECRET:
    print("✅ Secret appears to be in PEM format")
else:
    print("❌ Secret is NOT in PEM format")
    print("Please regenerate your keys at: https://cloud.coinbase.com/access/api")
