# Crypto Investment Insights

A simple AI-powered data analysis tool for cryptocurrency investment recommendations.

## Features

- Real-time crypto price data from CoinGecko API
- Technical analysis (moving averages, RSI, momentum)
- Simple buy/sell/hold recommendations
- Support for top cryptocurrencies

## Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-insights.git
cd crypto-insights

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
crypto-insights/
├── main.py              # Main application entry point
├── data_fetcher.py      # Fetch crypto data from APIs
├── analyzer.py          # Technical analysis logic
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Roadmap

- [ ] Basic CLI interface
- [ ] Technical indicators (SMA, RSI)
- [ ] Simple recommendation engine
- [ ] Web dashboard (Flask/Streamlit)
- [ ] Historical backtesting
- [ ] More advanced ML models

## License

MIT License
