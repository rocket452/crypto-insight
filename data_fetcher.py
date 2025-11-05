import requests
import pandas as pd
from datetime import datetime

class CryptoDataFetcher:
    """Fetch cryptocurrency data from CoinGecko API"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_top_cryptos(self, limit=10):
        """Get top cryptocurrencies by market cap"""
        url = f"{self.BASE_URL}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': False
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame(data)
            df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 
                     'total_volume', 'price_change_percentage_24h']]
            df.columns = ['id', 'symbol', 'name', 'price', 'market_cap', 
                         'volume_24h', 'change_24h']
            
            return df
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return pd.DataFrame()
    
    def get_historical_data(self, coin_id, days=30):
        """Get historical price data for a specific coin"""
        url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df[['date', 'price']]
            
            return df
        except Exception as e:
            print(f"Error fetching historical data for {coin_id}: {e}")
            return pd.DataFrame()
