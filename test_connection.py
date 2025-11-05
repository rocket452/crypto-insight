from coinbase_trader import CoinbaseTrader

def test_connection():
    """Test Coinbase CDP API connection"""
    print("Testing Coinbase CDP API connection...\n")
    
    trader = CoinbaseTrader()
    
    # Get all account balances
    print("\n--- All Account Balances ---")
    trader.get_accounts()
    
    # Get specific balances
    print("\n--- Specific Balances ---")
    trader.get_account_balance('USD')
    trader.get_account_balance('BTC')
    trader.get_account_balance('ETH')
    
    # Get current prices
    print("\n--- Current Prices ---")
    trader.get_product('BTC-USD')
    trader.get_product('ETH-USD')
    trader.get_product('SOL-USD')
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    test_connection()
