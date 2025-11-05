from coinbase_trader import CoinbaseTrader

def test_connection():
    """Test Coinbase API connection"""
    print("Testing Coinbase connection...\n")
    
    trader = CoinbaseTrader()
    
    # Get account balances
    print("\n--- Account Balances ---")
    trader.get_account_balance('USD')
    trader.get_crypto_balance('BTC')
    trader.get_crypto_balance('ETH')
    
    # Get current prices
    print("\n--- Current Prices ---")
    btc_price = trader.get_product_price('BTC-USD')
    if btc_price:
        print(f"BTC Price: ${btc_price:,.2f}")
    
    eth_price = trader.get_product_price('ETH-USD')
    if eth_price:
        print(f"ETH Price: ${eth_price:,.2f}")

if __name__ == "__main__":
    test_connection()
