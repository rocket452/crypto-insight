import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- FIX 1: Use consistent variable names for Coinbase Advanced Trade API ---
# These variables should contain the Key Name (ID) and the path to the private key file.
# We will use the common names: COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY_PATH

COINBASE_API_KEY_NAME = os.getenv("COINBASE_API_KEY_NAME")
COINBASE_PRIVATE_KEY_PATH = os.getenv("COINBASE_PRIVATE_KEY_PATH")

# --- FIX 2: Correct the validation block variable names ---
# The original code was validating COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY_PATH,
# but it was only retrieving COINBASE_API_KEY and COINBASE_API_SECRET above.
if not COINBASE_API_KEY_NAME or not COINBASE_PRIVATE_KEY_PATH:
    raise ValueError(
        "Missing credentials. Ensure .env contains COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY_PATH"
    )

print("✅ Config loaded successfully")
print(f"    API Key Name: {COINBASE_API_KEY_NAME}")
print(f"    Private Key Path: {COINBASE_PRIVATE_KEY_PATH}")

# Load and verify the private key JSON file
if not os.path.exists(COINBASE_PRIVATE_KEY_PATH):
    raise FileNotFoundError(f"❌ Private key file not found at: {COINBASE_PRIVATE_KEY_PATH}")

with open(COINBASE_PRIVATE_KEY_PATH, 'r') as f:
    try:
        key_data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("❌ Private key file is not valid JSON")

# Extract the PEM-encoded private key
COINBASE_PRIVATE_KEY = key_data.get('privateKey')
if not COINBASE_PRIVATE_KEY:
    raise ValueError("❌ 'privateKey' not found in JSON file")

print("✅ Private key loaded successfully")
# Note: Key ID is the name we loaded from the .env file (COINBASE_API_KEY_NAME),
# but sometimes the key file itself also contains an 'id' or 'name'.
# For clarity, we'll print the Key Name we loaded from the environment.
print(f"    Key ID: {COINBASE_API_KEY_NAME}")
print(f"    Private key preview: {COINBASE_PRIVATE_KEY[:50]}...")
