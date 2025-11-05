import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials
COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET')

# Validate that keys are loaded
if not COINBASE_API_KEY or not COINBASE_API_SECRET:
    raise ValueError("API credentials not found. Make sure .env file exists with COINBASE_API_KEY and COINBASE_API_SECRET")
