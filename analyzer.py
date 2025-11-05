import pandas as pd
import numpy as np

class CryptoAnalyzer:
    """Analyze cryptocurrency data and generate insights"""
    
    def calculate_sma(self, df, window=7):
        """Calculate Simple Moving Average"""
        return df['price'].rolling(window=window).mean()
    
    def calculate_rsi(self, df, period=14):
        """Calculate Relative Strength Index"""
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_momentum(self, df, period=10):
        """Calculate price momentum"""
        return df['price'].diff(period)
    
    def analyze_crypto(self, historical_df, current_data):
        """Perform technical analysis and generate recommendation"""
        if historical_df.empty:
            return None
        
        # Calculate indicators
        historical_df['sma_7'] = self.calculate_sma(historical_df, 7)
        historical_df['sma_20'] = self.calculate_sma(historical_df, 20)
        historical_df['rsi'] = self.calculate_rsi(historical_df)
        historical_df['momentum'] = self.calculate_momentum(historical_df)
        
        # Get latest values
        latest = historical_df.iloc[-1]
        current_price = current_data['price']
        
        # Generate signals
        signals = []
        score = 0
        
        # Moving average crossover
        if pd.notna(latest['sma_7']) and pd.notna(latest['sma_20']):
            if latest['sma_7'] > latest['sma_20']:
                signals.append("Bullish MA crossover")
                score += 1
            else:
                signals.append("Bearish MA crossover")
                score -= 1
        
        # RSI analysis
        if pd.notna(latest['rsi']):
            if latest['rsi'] < 30:
                signals.append("Oversold (RSI < 30)")
                score += 1
            elif latest['rsi'] > 70:
                signals.append("Overbought (RSI > 70)")
                score -= 1
        
        # Momentum
        if pd.notna(latest['momentum']) and latest['momentum'] > 0:
            signals.append("Positive momentum")
            score += 0.5
        elif pd.notna(latest['momentum']) and latest['momentum'] < 0:
            signals.append("Negative momentum")
            score -= 0.5
        
        # 24h change
        change_24h = current_data.get('change_24h', 0)
        if change_24h > 5:
            signals.append("Strong 24h gain")
            score += 0.5
        elif change_24h < -5:
            signals.append("Strong 24h loss")
            score -= 0.5
        
        # Generate recommendation
        if score >= 1.5:
            recommendation = "BUY"
            confidence = "High" if score >= 2.5 else "Medium"
        elif score <= -1.5:
            recommendation = "SELL"
            confidence = "High" if score <= -2.5 else "Medium"
        else:
            recommendation = "HOLD"
            confidence = "Low"
        
        return {
            'recommendation': recommendation,
            'confidence': confidence,
            'score': score,
            'signals': signals,
            'rsi': latest['rsi'] if pd.notna(latest['rsi']) else None,
            'sma_7': latest['sma_7'] if pd.notna(latest['sma_7']) else None,
            'sma_20': latest['sma_20'] if pd.notna(latest['sma_20']) else None
        }
```

## requirements.txt
```
pandas>=2.0.0
requests>=2.31.0
numpy>=1.24.0
