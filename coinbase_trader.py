from coinbase.rest import RESTClient
from config import COINBASE_API_KEY, COINBASE_API_SECRET

class CoinbaseTrader:
    """Execute trades on Coinbase"""
    
    def __init__(self):
        """Initialize with API credentials from environment"""
        self.client = RESTClient(
            api_key=COINBASE_API_KEY,
            api_secret=COINBASE_API_SECRET
        )
        print("✅ Connected to Coinbase")
    
    def get_accounts(self):
        """Get all account balances"""
        try:
            accounts = self.client.get_accounts()
            return accounts
        except Exception as e:
            print(f"❌ Error getting accounts: {e}")
            return None
    
    def get_account_balance(self, currency='USD'):
        """Get account balance for a specific currency"""
        try:
            accounts = self.client.get_accounts()
            for account in accounts.get('accounts', []):
                if account['currency'] == currency:
                    balance = float(account['available_balance']['value'])
                    print(f"💰 {currency} Balance: ${balance:,.2f}")
                    return balance
            return 0.0
        except Exception as e:
            print(f"❌ Error getting balance: {e}")
            return None
    
    def get_crypto_balance(self, currency='BTC'):
        """Get crypto balance"""
        try:
            accounts = self.client.get_accounts()
            for account in accounts.get('accounts', []):
                if account['currency'] == currency:
                    balance = float(account['available_balance']['value'])
                    print(f"💰 {currency} Balance: {balance:.6f}")
                    return balance
            return 0.0
        except Exception as e:
            print(f"❌ Error getting crypto balance: {e}")
            return None
    
    def market_buy(self, product_id, usd_amount):
        """
        Place a market buy order
        product_id: e.g., 'BTC-USD', 'ETH-USD'
        usd_amount: amount in USD to spend
        """
        try:
            print(f"🔄 Placing buy order: ${usd_amount} of {product_id}")
            order = self.client.market_order_buy(
                product_id=product_id,
                quote_size=str(usd_amount)
            )
            print(f"✅ Buy order placed successfully")
            return order
        except Exception as e:
            print(f"❌ Error placing buy order: {e}")
            return None
    
    def market_sell(self, product_id, crypto_amount):
        """
        Place a market sell order
        product_id: e.g., 'BTC-USD'
        crypto_amount: amount of crypto to sell
        """
        try:
            print(f"🔄 Placing sell order: {crypto_amount} {product_id}")
            order = self.client.market_order_sell(
                product_id=product_id,
                base_size=str(crypto_amount)
            )
            print(f"✅ Sell order placed successfully")
            return order
        except Exception as e:
            print(f"❌ Error placing sell order: {e}")
            return None
    
    def get_product_price(self, product_id):
        """Get current price for a product"""
        try:
            product = self.client.get_product(product_id)
            price = float(product['price'])
            return price
        except Exception as e:
            print(f"❌ Error getting price: {e}")
            return None
