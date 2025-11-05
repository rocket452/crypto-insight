#!/usr/bin/env python3
"""
Crypto Investment Insights - Simple AI-powered crypto analysis tool
"""

from data_fetcher import CryptoDataFetcher
from analyzer import CryptoAnalyzer
import time

def print_header():
    print("\n" + "="*60)
    print("  CRYPTO INVESTMENT INSIGHTS")
    print("="*60 + "\n")

def print_analysis(crypto_data, analysis):
    """Print formatted analysis for a cryptocurrency"""
    print(f"\n{'─'*60}")
    print(f"  {crypto_data['name']} ({crypto_data['symbol'].upper()})")
    print(f"{'─'*60}")
    print(f"  Current Price:   ${crypto_data['price']:,.2f}")
    print(f"  24h Change:      {crypto_data['change_24h']:+.2f}%")
    print(f"  Market Cap:      ${crypto_data['market_cap']:,.0f}")
    
    if analysis:
        print(f"\n  📊 Technical Indicators:")
        if analysis['rsi']:
            print(f"     RSI:          {analysis['rsi']:.1f}")
        if analysis['sma_7']:
            print(f"     SMA (7d):     ${analysis['sma_7']:,.2f}")
        if analysis['sma_20']:
            print(f"     SMA (20d):    ${analysis['sma_20']:,.2f}")
        
        print(f"\n  🎯 Recommendation: {analysis['recommendation']}")
        print(f"  🔍 Confidence:     {analysis['confidence']}")
        print(f"  📈 Score:          {analysis['score']:.1f}")
        
        print(f"\n  💡 Signals:")
        for signal in analysis['signals']:
            print(f"     • {signal}")
    else:
        print("\n  ⚠️  Insufficient data for analysis")

def main():
    print_header()
    print("Fetching cryptocurrency data...\n")
    
    fetcher = CryptoDataFetcher()
    analyzer = CryptoAnalyzer()
    
    # Get top cryptocurrencies
    top_cryptos = fetcher.get_top_cryptos(limit=5)
    
    if top_cryptos.empty:
        print("❌ Failed to fetch cryptocurrency data. Please check your internet connection.")
        return
    
    print(f"Analyzing top {len(top_cryptos)} cryptocurrencies...\n")
    
    recommendations = {'BUY': [], 'SELL': [], 'HOLD': []}
    
    # Analyze each cryptocurrency
    for idx, row in top_cryptos.iterrows():
        print(f"Analyzing {row['name']}...")
        
        # Get historical data
        historical = fetcher.get_historical_data(row['id'], days=30)
        
        # Perform analysis
        analysis = analyzer.analyze_crypto(historical, row)
        
        # Print detailed analysis
        print_analysis(row, analysis)
        
        if analysis:
            recommendations[analysis['recommendation']].append({
                'name': row['name'],
                'symbol': row['symbol'],
                'price': row['price'],
                'confidence': analysis['confidence']
            })
        
        # Rate limiting - be nice to the API
        time.sleep(1)
    
    # Print summary
    print(f"\n\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}\n")
    
    for action in ['BUY', 'SELL', 'HOLD']:
        if recommendations[action]:
            print(f"  {action}:")
            for crypto in recommendations[action]:
                conf_emoji = "🔥" if crypto['confidence'] == "High" else "⚡" if crypto['confidence'] == "Medium" else "💤"
                print(f"    {conf_emoji} {crypto['name']} ({crypto['symbol'].upper()}) - ${crypto['price']:,.2f}")
        else:
            print(f"  {action}: None")
        print()
    
    print(f"{'='*60}")
    print("\n⚠️  Disclaimer: This is for educational purposes only.")
    print("   Always do your own research before investing.\n")

if __name__ == "__main__":
    main()
