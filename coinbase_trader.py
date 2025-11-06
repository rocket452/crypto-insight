import os
import json
import asyncio
# Import Decimal for accurate financial calculations
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv

# Coinbase Advanced Trade API client (RESTClient)
from coinbase.rest import RESTClient 

# Coinbase Developer Platform client (CdpClient) - Used for EVM/Solana features
from cdp import CdpClient 

# Assuming 'from config import COINBASE_API_KEY, COINBASE_API_SECRET' is correct.
# COINBASE_API_KEY is the Key Name (ID), COINBASE_API_SECRET is the Private Key Content.
from config import COINBASE_API_KEY, COINBASE_API_SECRET

# Load environment variables from .env file (if used for other variables)
load_dotenv()

# --- Advanced Trade API Client Class ---
# This class handles synchronous trading/balance operations using RESTClient.
class CoinbaseTrader:
    """Execute trades and retrieve balances on Coinbase using the Advanced Trade REST API."""

    def __init__(self):
        """Initializes the synchronous RESTClient."""
        
        # The COINBASE_API_SECRET must be the processed string with actual newlines (\n).
        # Assuming the 'config' module has already handled the '.replace('\\n', '\n')' logic.
        self.client = RESTClient(api_key=COINBASE_API_KEY, api_secret=COINBASE_API_SECRET)
        
        print("✅ Connected to Coinbase Advanced Trade API")

    # --- Methods below are correctly formatted for RESTClient and Decimal handling ---

    def get_accounts(self):
        """Retrieve all account balances"""
        try:
            accounts = self.client.get_accounts()
            print("\n💰 All Account Balances:")
            
            for account in accounts.get('accounts', []):
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
            
    def get_product(self, product_id='BTC-USD'):
        """Retrieve current market info (ticker) for a product"""
        try:
            # get_product_ticker is the correct RESTClient method for current price.
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

# --- Asynchronous CDP Client Logic (If needed) ---
async def cdp_test():
    """Initializes and tests the asynchronous CDP Client connection."""
    try:
        # Using a context manager ensures the client is closed automatically
        async with CdpClient() as cdp:
            print("✅ CDP Client connection successful.")
            # Add actual CDP methods here if you intend to use them, e.g.:
            # accounts = await cdp.evm.list_accounts()
            # print(f"CDP EVM Accounts: {len(accounts.accounts)}")
    except Exception as e:
        print(f"❌ Error connecting to CDP: {e}")

# --- Main Execution Flow ---
def run_trader_tests():
    """Synchronous test of the Advanced Trade API."""
    print("\n--- Starting Advanced Trade API Tests ---")
    trader = CoinbaseTrader()
    
    trader.get_accounts()
    trader.get_account_balance('USD')
    trader.get_product('BTC-USD')
    trader.get_product('ETH-USD')
    
    print("\n--- Advanced Trade API Tests Complete ---")

if __name__ == '__main__':
    # Run the synchronous Advanced Trade API tests
    run_trader_tests()
    
    # If you need to test the asynchronous CDP client, run it separately
    # asyncio.run(cdp_test())
