# 💹 Crypto Investment Insights with CDP Trading

An **AI-powered cryptocurrency analysis tool** that provides intelligent trading insights and can execute trades automatically via **Coinbase Developer Platform (CDP)**.

---

## 🚀 Features

- 📊 Real-time crypto price data and analysis  
- 📈 Technical indicators (slippage, liquidity, swap rates)  
- 🤖 **AI-powered buy/sell/hold recommendations**  
- 🧠 **Local AI model for private, cost-free analysis**  
- 💱 Automatic trade execution via CDP  
- 🔐 Secure wallet management  
- ⚡ **Real-time trading insights generation**

---

## ⚙️ Setup Instructions

### 🧩 Prerequisites

- Python 3.10 or higher  
- A Coinbase Developer Platform account  
- **No external AI API keys required** (uses local AI)

---

### 🪄 Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/crypto-insights.git
cd crypto-insights
🧰 Step 2: Install Dependencies
bash
Copy code
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
🔑 Step 3: Generate CDP API Keys
Go to the CDP Portal → https://portal.cdp.coinbase.com/projects

Create a new project (or select an existing one)

Navigate to API Keys in the left sidebar

Click Create API Key

Configure your key:

Name: crypto-insights (or your preferred name)

IP Allowlist: 0.0.0.0/0 for testing (restrict in production)

Permissions: View (read-only) and Trade

Signature Algorithm: Ed25519 (recommended)

Click Create

Download the JSON file and save it as cdp_api_key.json in your project folder

🪙 Step 4: Generate Wallet Secret
In the CDP Portal, go to Server Wallet in the left sidebar

Click Generate in the Wallet Secret section

Copy the secret and save it securely (you won’t be able to see it again!)

⚙️ Step 5: Create Configuration Files
.env File
Create a file named .env in your project root:

env
Copy code
CDP_WALLET_SECRET=your-wallet-secret-here
Replace your-wallet-secret-here with the wallet secret you generated in Step 4.

cdp_api_key.json File
Your file should look like this:

json
Copy code
{
  "id": "organizations/xxxxx-xxxx-xxxx-xxxx/apiKeys/yyyyy-yyyy-yyyy-yyyy",
  "privateKey": "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEI...\n-----END EC PRIVATE KEY-----"
}
▶️ Step 6: Run the Application
bash
Copy code
python main_simple.py
First run will:

Initialize CDP connection

Analyze market conditions

Generate AI-powered trading insights

Provide BUY/SELL/HOLD recommendations with confidence levels

📁 File Structure
text
Copy code
crypto-insights/
├── .env                     # Your wallet secret (DO NOT COMMIT)
├── .gitignore               # Git ignore rules
├── cdp_api_key.json         # Your CDP API credentials (DO NOT COMMIT)
├── main_simple.py           # Main application with AI insights
├── simple_llm_reliable.py   # AI trading intelligence engine
├── requirements.txt         # Python dependencies
└── README.md                # This file
🧠 AI Trading Insights
Technical Analysis
Slippage Analysis: Measures execution quality (0–2% optimal, 2%+ caution)

Liquidity Assessment: Evaluates market depth and execution efficiency

Swap Rate Optimization: Analyzes current exchange rates

AI Decision Making
The local AI model analyzes:

Market conditions in real time

Technical indicators from CDP data

Risk assessment and confidence scoring

Actionable BUY/SELL/HOLD recommendations

📊 Sample Output
text
Copy code
🤖 AI TRADING ADVICE:
  Recommendation: BUY
  Confidence: HIGH
  Model: IntelligentTradingAI-v1

  Analysis: Strong buy signal with optimal liquidity conditions and minimal slippage. 
  Good entry point for position. Current slippage: 0.15%, Liquidity: Excellent.
🧩 Usage
Run AI-Powered Analysis
bash
Copy code
python main_simple.py
Expected Output:

✅ CDP connection status

🔧 Technical analysis (slippage, liquidity, swap rates)

🧠 AI trading recommendations with confidence levels

💡 Actionable insights for trading decisions

📈 Example Trading Scenarios
Optimal Conditions (BUY):
Slippage < 0.5% + Excellent liquidity → HIGH confidence BUY

Caution Required (SELL):
Slippage > 2.0% + Poor liquidity → MEDIUM confidence SELL

Neutral Market (HOLD):
Mixed indicators → MEDIUM confidence HOLD

⚙️ Configuration
.env File Format
env
Copy code
CDP_WALLET_SECRET=your-wallet-secret-from-cdp-portal
cdp_api_key.json File Format
json
Copy code
{
  "id": "organizations/YOUR-ORG-ID/apiKeys/YOUR-KEY-ID",
  "privateKey": "-----BEGIN EC PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END EC PRIVATE KEY-----"
}
Required Fields:

id – Your API key identifier (from CDP)

privateKey – Your private key for signing requests

🤖 AI Features
Intelligent Trading Assistant
No API costs – uses local AI model

Privacy-focused – data stays on your machine

Real-time analysis – instant insights

Confidence scoring – understand certainty of recommendations

Analysis Capabilities
Liquidity quality assessment

Slippage risk evaluation

Market condition scoring

Trade timing recommendations

🔗 Important Links
CDP Portal: https://portal.cdp.coinbase.com/projects

CDP Documentation: https://docs.cdp.coinbase.com/

API Keys Dashboard: (select your project → API Keys)

Server Wallet Dashboard: (select your project → Server Wallet)

🔒 Security Best Practices
Never commit secrets — add .env and cdp_api_key.json to .gitignore

Use IP allowlists — restrict access to your IP

Start small — test with minimal funds

Use read-only keys first — for safe testing

Rotate keys regularly

Store secrets securely — use environment variables or secret managers

🛠️ Troubleshooting
Error: “Wallet Secret not configured”

Ensure .env contains CDP_WALLET_SECRET

Verify .env is in the same directory as your script

Confirm Wallet Secret is generated from CDP Portal

Error: “401 Unauthorized”

Check your IP allowlist (use 0.0.0.0/0 for testing)

Ensure cdp_api_key.json is in the correct location

Verify your API key permissions

Wait a few minutes after adding your IP

Error: “python-dotenv could not parse statement”

Check for syntax errors in .env

No quotes or spaces around =

Format must be KEY=value

⚠️ Disclaimer
This tool is for educational purposes only.
Cryptocurrency trading carries significant risk.
Never invest more than you can afford to lose.
Past performance does not guarantee future results.
Always do your own research (DYOR).
This is not financial advice.

📜 License
MIT License

💬 Support
For code issues → Open an issue on GitHub

For CDP API questions → CDP Docs

For Coinbase account issues → Coinbase Support

yaml
Copy code
