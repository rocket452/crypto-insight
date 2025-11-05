import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials for Coinbase Advanced Trade API
# COINBASE_API_KEY_NAME is typically the Key ID (e.g., '1a2b3c4d')
COINBASE_API_KEY_NAME = os.getenv("COINBASE_API_KEY_NAME")

# --- FIX: Change variable name to COINBASE_API_SECRET ---
# We now expect the raw private key content to be in the COINBASE_API_SECRET variable.
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET")

# Validate that environment variables are set
if not COINBASE_API_KEY_NAME or not COINBASE_API_SECRET:
    # --- FIX: Update error message to reflect the new variable name ---
    raise ValueError(
        "Missing credentials. Ensure .env contains COINBASE_API_KEY_NAME and COINBASE_API_SECRET"
    )

print("✅ Config loaded successfully")
print(f"    API Key Name: {COINBASE_API_KEY_NAME}")
# --- FIX: Update print statement for the new variable ---
print(f"    Private Key Preview: {COINBASE_API_SECRET[:50]}...")

# --- REMOVE: The file loading logic is no longer needed since the key is loaded directly ---
# The original code for loading and verifying the JSON file has been removed, 
# as we assume COINBASE_API_SECRET now holds the raw PEM string.

# The final variable used for the Coinbase client will be COINBASE_API_SECRET.
# If your COINBASE_API_SECRET variable contains the full JSON file content 
# from the Advanced Trade API, you would need to parse it here:

try:
    # Attempt to load the value as JSON, assuming the private key content 
    # might be the full JSON object including the "privateKey" field.
    key_data = json.loads(COINBASE_API_SECRET)
    
    # Extract the PEM-encoded private key from the JSON
    # This assumes the value of COINBASE_API_SECRET in your .env is the full JSON payload
    COINBASE_API_SECRET = key_data.get('privateKey')
    
    if not COINBASE_API_SECRET:
        raise ValueError("❌ 'privateKey' not found in COINBASE_API_SECRET JSON data.")

except json.JSONDecodeError:
    # If it's not JSON, assume COINBASE_API_SECRET is already the raw PEM string.
    # This is often simpler and better practice for .env files.
    pass

print("✅ Private key processed successfully")
