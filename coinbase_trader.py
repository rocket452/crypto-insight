import os
import json
# Import Decimal for accurate financial calculations
from decimal import Decimal, InvalidOperation

# Assuming 'from config import COINBASE_API_KEY, COINBASE_API_SECRET' is correct
# and COINBASE_API_KEY and COINBASE_API_SECRET are correctly imported
from coinbase.rest import RESTClient
from config import COINBASE_API_KEY, COINBASE_API_SECRET # Keep this line as per the original

class CoinbaseTrader:
    """Execute trades on Coinbase using the Advanced Trade API"""

    def __init__(self):
        """Initialize with credentials loaded from config.py"""
        # Ensure your COINBASE_API_KEY and COINBASE_API_SECRET are the KEY_NAME and PRIVATE_KEY
        # from the previous fixation if you are using the Advanced Trade API.
 #       self.client = RESTClient(
#            api_key=COINBASE_API_KEY,
 #           api_secret=COINBASE_API_SECRET
   #     )
        
        self.client = CDPClient(
            api_key_name=COINBASE_API_KEY,
            private_key=COINBASE_API_SECRET
        )
        print("✅ Connected to Coinbase Advanced Trade API")

    # --- FIX 1: Use Decimal for balances for precision ---
    def get_accounts(self):
        """Retrieve all account balances"""
        try:
            accounts = self.client.get_accounts()
            print("\n💰 All Account Balances:")
            
            # The API response structure can sometimes be in the 'accounts' key
            for account in accounts.get('accounts', []):
                # Use Decimal to handle the string value for precision
                balance_str = account.get('available_balance', {}).get('value', '0')
                currency = account.get('currency', 'UNKNOWN')
                
                try:
                    balance = Decimal(balance_str)
                except InvalidOperation:
                    print(f"⚠️ Skipping {currency}: Invalid balance value '{balance_str}'")
                    continue
                
                if balance > Decimal('0'):
                    # Format output with correct precision
                    print(f"    {currency}: {balance:f}") 
            return accounts
        except Exception as e:
            print(f"❌ Error getting accounts: {e}")
            return None

    # --- FIX 2: Use Decimal for specific balance for precision ---
    def get_account_balance(self, currency='USD'):
        """Retrieve available balance for a specific currency"""
        try:
            accounts = self.client.get_accounts()
            for account in accounts.get('accounts', []):
                if account.get('currency') == currency:
                    balance_str = account.get('available_balance', {}).get('value', '0')
                    
                    try:
                        balance = Decimal(balance_str)
                    except InvalidOperation:
                        print(f"⚠️ Invalid balance value for {currency}: '{balance_str}'")
                        return Decimal('0')
                        
                    print(f"💰 {currency} Available Balance: {balance:f}")
                    return balance
            
            print(f"ℹ️  No {currency} account found or balance is zero.")
            return Decimal('0')
        except Exception as e:
            print(f"❌ Error getting {currency} balance: {e}")
            return None
            
    # --- FIX 3: Get 'price' from the expected location in the API response ---
    def get_product(self, product_id='BTC-USD'):
        """Retrieve current market info (ticker) for a product"""
        try:
            # The get_product endpoint often returns market data in a 'product' key.
            # However, the correct way to get the current price/ticker is generally 
            # the get_product_ticker endpoint, which has a 'price' key directly in its response.
            # Assuming you want the Ticker data here:
            product_ticker = self.client.get_product_ticker(product_id)
            
            # Use Decimal for price to preserve accuracy
            price = Decimal(product_ticker['price'])
            print(f"📈 {product_id} Price: ${price:,.2f}")
            return product_ticker
            
        except Exception as e:
            print(f"❌ Error getting {product_id} ticker: {e}")
            return None

    def market_buy(self, product_id, usd_amount: Decimal):
        """Place a market buy order (quote_size is in terms of the quote currency, e.g., USD)"""
        try:
            # Type hint added for clarity that usd_amount should be Decimal or convertible
            print(f"⚠️  Placing market buy order: ${usd_amount:f} worth of {product_id}")
            order = self.client.market_order_buy(
                product_id=product_id,
                # Convert Decimal back to string for the API call
                quote_size=str(usd_amount) 
            )
            print("✅ Buy order placed successfully")
            return order
        except Exception as e:
            print(f"❌ Error placing buy order: {e}")
            return None

    def market_sell(self, product_id, crypto_amount: Decimal):
        """Place a market sell order (base_size is in terms of the base currency, e.g., BTC)"""
        try:
            # Type hint added for clarity that crypto_amount should be Decimal or convertible
            print(f"⚠️  Placing market sell order: {crypto_amount:f} {product_id}")
            order = self.client.market_order_sell(
                product_id=product_id,
                # Convert Decimal back to string for the API call
                base_size=str(crypto_amount)
            )
            print("✅ Sell order placed successfully")
            return order
        except Exception as e:
            print(f"❌ Error placing sell order: {e}")
            return None

# Example Usage (optional block you would run outside the class definition)
# if __name__ == '__main__':
#     # NOTE: The values in config.py must be set correctly for this to work.
#     # COINBASE_API_KEY should be the Key Name (ID)
#     # COINBASE_API_SECRET should be the Private Key (the full PEM string)
#     trader = CoinbaseTrader()
#     trader.get_accounts()
#     trader.get_account_balance('USD')
#     trader.get_product('BTC-USD')
#     # Example of placing a market buy for $10 USD worth of BTC (assuming enough funds)
#     # trader.market_buy('BTC-USD', Decimal('10'))
