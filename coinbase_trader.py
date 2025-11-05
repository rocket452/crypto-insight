from coinbase.wallet.client import Client
from config import COINBASE_API_KEY, COINBASE_API_SECRET

class CoinbaseTrader:
    def __init__(self):
        self.client = Client(COINBASE_API_KEY, COINBASE_API_SECRET)
        print("✅ Connected to Coinbase")
    
    def get_all_accounts(self):
        """Get all accounts with balances"""
        try:
            accounts = self.client.get_accounts()
            print("\n💰 All Account Balances:")
            for account in accounts.data:
                balance = float(account['balance']['amount'])
                currency = account['currency']
                if balance > 0:  # Only show non-zero balances
                    print(f"   {currency}: {balance:.8f}")
            return accounts
        except Exception as e:
            print(f"❌ Error getting accounts: {e}")
            return None
    
    def get_account_balance(self, currency='USD'):
        """Get balance for a specific currency"""
        try:
            accounts = self.client.get_accounts()
            for account in accounts.data:
                if account['currency'] == currency:
                    balance = float(account['balance']['amount'])
                    print(f"💰 {currency} Balance: {balance:.8f}")
                    return balance
            print(f"ℹ️  No {currency} account found")
            return 0.0
        except Exception as e:
            print(f"❌ Error getting {currency} balance: {e}")
            return None
    
    def get_spot_price(self, currency_pair='BTC-USD'):
        """Get current spot price"""
        try:
            price = self.client.get_spot_price(currency_pair=currency_pair)
            price_value = float(price['amount'])
            print(f"📈 {currency_pair} Price: ${price_value:,.2f}")
            return price_value
        except Exception as e:
            print(f"❌ Error getting {currency_pair} price: {e}")
            return None
    
    def buy_crypto(self, account_id, amount, currency='BTC'):
        """Buy crypto (use with caution!)"""
        try:
            print(f"⚠️  Attempting to buy {amount} {currency}")
            buy = self.client.buy(
                account_id,
                amount=amount,
                currency=currency,
                commit=True
            )
            print(f"✅ Buy order successful: {buy}")
            return buy
        except Exception as e:
            print(f"❌ Error placing buy order: {e}")
            return None
    
    def sell_crypto(self, account_id, amount, currency='BTC'):
        """Sell crypto (use with caution!)"""
        try:
            print(f"⚠️  Attempting to sell {amount} {currency}")
            sell = self.client.sell(
                account_id,
                amount=amount,
                currency=currency,
                commit=True
            )
            print(f"✅ Sell order successful: {sell}")
            return sell
        except Exception as e:
            print(f"❌ Error placing sell order: {e}")
            return None
