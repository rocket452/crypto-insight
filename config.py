import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials for CDP API
COINBASE_API_KEY_NAME = os.getenv('COINBASE_API_KEY_NAME')
COINBASE_PRIVATE_KEY_PATH = os.getenv('COINBASE_PRIVATE_KEY_PATH')

# Validate that keys are loaded
if not COINBASE_API_KEY_NAME or not COINBASE_PRIVATE_KEY_PATH:
    raise ValueError("API credentials not found. Make sure .env file exists with COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY_PATH")

# Print for debugging
print(f"✅ Config loaded successfully")
print(f"   API Key Name: {COINBASE_API_KEY_NAME}")
print(f"   Private Key Path: {COINBASE_PRIVATE_KEY_PATH}")

# Verify the JSON file exists and can be read
if os.path.exists(COINBASE_PRIVATE_KEY_PATH):
    print(f"✅ Private key file found")
    try:
        with open(COINBASE_PRIVATE_KEY_PATH, 'r') as f:
            key_data = json.load(f)
            # CDP API uses "id" not "name"
            key_id = key_data.get('id') or key_data.get('name')
            print(f"   Key ID from file: {key_id[:50] if key_id else 'NOT FOUND'}...")
            print(f"   Private key present: {'Yes' if 'privateKey' in key_data else 'No'}")
            
            # Show first few characters of private key to verify format
            if 'privateKey' in key_data:
                COINBASE_PRIVATE_KEY_PATH = key_data['privateKey']
                pk_preview = key_data['privateKey'][:50]
                print(f"   Private key starts with: {pk_preview}...")
    except Exception as e:
        print(f"⚠️  Error reading key file: {e}")
else:
    print(f"❌ Private key file NOT found at: {COINBASE_PRIVATE_KEY_PATH}")
