import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials for CDP API
COINBASE_API_KEY_NAME = os.getenv('COINBASE_API_KEY_NAME')
COINBASE_PRIVATE_KEY_PATH = os.getenv('COINBASE_PRIVATE_KEY_PATH')

# Validate that keys are loaded
if not COINBASE_API_KEY_NAME or not COINBASE_PRIVATE_KEY_PATH:
    raise ValueError("API credentials not found. Make sure .env file exists with COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY_PATH")
```

## Step 2: Update `.env`

After you create the key and download the JSON file, your `.env` should look like:
```
COINBASE_API_KEY_NAME=organizations/your-org-id/apiKeys/your-key-id
COINBASE_PRIVATE_KEY_PATH=F:\Projects\crypto-insight\cdp_api_key.json
