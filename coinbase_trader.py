from coinbase.rest import RESTClient
from config import COINBASE_API_KEY, COINBASE_API_SECRET

class CoinbaseTrader:
    """Execute trades on Coinbase using the Advanced Trade API"""

    def __init__(self):
        """Initialize with credentials loaded from config.py"""
        self.client = RESTClient(
            api_key=COINBASE_API_KEY,
            api_secret=COINBASE_API_SECRET
        )
        print("✅ Connected to Coinbase Advanced Trade API")

    def get_accounts(self):
        """Retrieve all account balances"""
        try:
            accounts = self.client.get_accounts()
            print("\n💰 All Account Balances:")
            for account in accounts['accounts']:
                balance = float(account['available_balance']['value'])
                currency = account['currency']
                if balance > 0:
                    print(f"   {currency}: {balance:.8f}")
            return accounts
        except Exception as e:
            print(f"❌ Error getting accounts: {e}")
            return None

    def get_account_balance(self, currency='USD'):
        """Retrieve balance for a specific currency"""
        try:
            accounts = self.client.get_accounts()
            for account in accounts.get('accounts', []):
                if account['currency'] == currency:
                    balance = float(account['available_balance']['value'])
                    print(f"💰 {currency} Balance: {balance:.8f}")
                    return balance
            print(f"ℹ️  No {currency} account found")
            return 0.0
        except Exception as e:
            print(f"❌ Error getting {currency} balance: {e}")
            return None

    def get_product(self, product_id='BTC-USD'):
        """Retrieve current market info for a product"""
        try:
            product = self.client.get_product(product_id)
            price = float(product['price'])
            print(f"📈 {product_id} Price: ${price:,.2f}")
            return product
        except Exception as e:
            print(f"❌ Error getting {product_id}: {e}")
            return None

    def market_buy(self, product_id, usd_amount):
        """Place a market buy order"""
        try:
            print(f"⚠️  Placing buy order: ${usd_amount} of {product_id}")
            order = self.client.market_order_buy(
                product_id=product_id,
                quote_size=str(usd_amount)
            )
            print("✅ Buy order placed successfully")
            return order
        except Exception as e:
            print(f"❌ Error placing buy order: {e}")
            return None

    def market_sell(self, product_id, crypto_amount):
        """Place a market sell order"""
        try:
            print(f"⚠️  Placing sell order: {crypto_amount} {product_id}")
            order = self.client.market_order_sell(
                product_id=product_id,
                base_size=str(crypto_amount)
            )
            print("✅ Sell order placed successfully")
            return order
        except Exception as e:
            print(f"❌ Error placing sell order: {e}")
            return None
