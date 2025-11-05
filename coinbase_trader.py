from coinbase.wallet.client import Client
from config import COINBASE_API_KEY, COINBASE_API_SECRET

class CoinbaseTrader:
    def __init__(self):
        self.client = Client(COINBASE_API_KEY, COINBASE_API_SECRET)
        print("✅ Connected to Coinbase")
    
    def get_accounts(self):
        """Get all accounts"""
        try:
            accounts = self.client.get_accounts()
            return accounts
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_account_balance(self, currency='USD'):
        """Get balance for a currency"""
        try:
            accounts = self.client.get_accounts()
            for account in accounts.data:
                if account['currency'] == currency:
                    balance = float(account['balance']['amount'])
                    print(f"💰 {currency} Balance: ${balance:,.2f}")
                    return balance
            return 0.0
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_spot_price(self, currency_pair='BTC-USD'):
        """Get current spot price"""
        try:
            price = self.client.get_spot_price(currency_pair=currency_pair)
            return float(price['amount'])
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def buy_crypto(self, account_id, amount, currency='BTC'):
        """Buy crypto (use with caution!)"""
        try:
            buy = self.client.buy(
                account_id,
                amount=amount,
                currency=currency,
                commit=True
            )
            print(f"✅ Buy order: {buy}")
            return buy
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
