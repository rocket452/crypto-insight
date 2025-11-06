from coinbase.rest import RESTClient
import json

API_KEY = os.environ.get('CDP_API_KEY_ID')
API_SECRET = os.environ.get('CDP_API_KEY_SECRET')

# Initialize client
client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Get account balances
accounts = client.get_accounts()

# Print all balances
print("Coinbase Account Balances:")
for account in accounts['accounts']:
    balance = float(account['available_balance']['value'])
    if balance > 0:
        currency = account['available_balance']['currency']
        print(f"{currency}: {balance}")

# Get specific currency balance
def get_balance(currency='BTC'):
    accounts = client.get_accounts()
    for account in accounts['accounts']:
        if account['available_balance']['currency'] == currency:
            return float(account['available_balance']['value'])
    return 0

btc_balance = get_balance('BTC')
print(f"BTC Balance: {btc_balance}")
