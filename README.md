<img width="1085" height="312" alt="image" src="https://github.com/user-attachments/assets/38bf6889-7c22-4194-a745-560a03f1695c" />


````markdown
# 💹 Crypto Investment Insights with CDP Trading

An **AI-powered cryptocurrency analysis tool** that provides intelligent trading insights and can execute trades automatically via **Coinbase Developer Platform (CDP)**.

---

## ✨ Features

* 📊 **Real-time crypto price data and analysis**
* 📈 Technical indicators analysis (slippage, liquidity, swap rates)
* 🤖 **AI-powered buy/sell/hold recommendations**
* 🧠 **Local AI model for private, cost-free analysis**
* 💱 Automatic trade execution via CDP
* 🔐 Secure wallet management
* ⚡ Real-time trading insights generation

---

## ⚙️ Setup Instructions

### 🧩 Prerequisites

* Python 3.10 or higher
* A Coinbase Developer Platform (CDP) account
* **No external AI API keys required** (uses local AI)

### 🪄 Step 1: Clone the Repository

```bash
git clone [https://github.com/yourusername/crypto-insights.git](https://github.com/yourusername/crypto-insights.git)
cd crypto-insights
````

### 🧰 Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 🔑 Step 3: Generate CDP API Keys

1.  Go to the CDP Portal: **`https://portal.cdp.coinbase.com/projects`**
2.  Create a new project (or select an existing one).
3.  Navigate to **API Keys** in the left sidebar.
4.  Click **Create API Key**.
5.  **Configure your key:**
      * **Name:** `crypto-insights` (or your preferred name)
      * **IP Allowlist:** `0.0.0.0/0` for testing (restrict in production)
      * **Permissions:** `View` (read-only) and `Trade`
      * **Signature Algorithm:** `Ed25519` (recommended)
6.  Click **Create**.
7.  **Download the JSON file** and save it as **`cdp_api_key.json`** in your project folder.

### 🪙 Step 4: Generate Wallet Secret

1.  In the CDP Portal, go to **Server Wallet** in the left sidebar.
2.  Click **Generate** in the Wallet Secret section.
3.  **Copy the secret and save it securely** (you won’t be able to see it again\!).

### ⚙️ Step 5: Create Configuration Files

#### `.env` File

Create a file named `.env` in your project root:

```env
CDP_WALLET_SECRET=your-wallet-secret-here
```

*Replace `your-wallet-secret-here` with the wallet secret you generated in Step 4.*

#### `cdp_api_key.json` File

This file was downloaded in Step 3 and should look like this (but with your unique credentials):

```json
{
  "id": "organizations/xxxxx-xxxx-xxxx-xxxx/apiKeys/yyyyy-yyyy-yyyy-yyyy",
  "privateKey": "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEI...\n-----END EC PRIVATE KEY-----"
}
```

### ▶️ Step 6: Run the Application

```bash
python main_simple.py
```

**First run will:**

  * Initialize CDP connection.
  * Analyze market conditions.
  * Generate AI-powered trading insights.
  * Provide `BUY`/`SELL`/`HOLD` recommendations with confidence levels.

-----

## 📁 File Structure

```text
crypto-insights/
├── .env                     # Your wallet secret (DO NOT COMMIT)
├── .gitignore               # Git ignore rules
├── cdp_api_key.json         # Your CDP API credentials (DO NOT COMMIT)
├── main_simple.py           # Main application with AI insights
├── simple_llm_reliable.py   # AI trading intelligence engine
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

-----

## 🧠 AI Trading Insights

The local AI model provides sophisticated trading insights by analyzing two main components:

### Technical Analysis

  * **Slippage Analysis:** Measures execution quality (`0–2% optimal`, `2%+ caution`).
  * **Liquidity Assessment:** Evaluates market depth and execution efficiency.
  * **Swap Rate Optimization:** Analyzes current exchange rates for best trade execution.

### AI Decision Making

The local AI model combines **real-time market conditions** and **technical indicators from CDP data** to perform **risk assessment and confidence scoring**, ultimately generating **actionable BUY/SELL/HOLD recommendations**.

### 📊 Sample Output

```text
🤖 AI TRADING ADVICE:
  Recommendation: BUY
  Confidence: HIGH
  Model: IntelligentTradingAI-v1

  Analysis: Strong buy signal with optimal liquidity conditions and minimal slippage.
  Good entry point for position. Current slippage: 0.15%, Liquidity: Excellent.
```

-----

## 💡 Usage

### Run AI-Powered Analysis

```bash
python main_simple.py
```

**Expected Output Includes:**

  * ✅ CDP connection status
  * 🔧 Technical analysis (slippage, liquidity, swap rates)
  * 🧠 AI trading recommendations with confidence levels
  * 💡 Actionable insights for trading decisions

### 📈 Example Trading Scenarios

| Conditions | Recommendation | Confidence | Rationale |
| :--- | :--- | :--- | :--- |
| Slippage \< 0.5% + Excellent liquidity | **BUY** | HIGH | Optimal entry point. |
| Slippage \> 2.0% + Poor liquidity | **SELL** | MEDIUM | Caution required; high risk of poor execution. |
| Mixed indicators | **HOLD** | MEDIUM | Neutral market; wait for clearer signal. |

-----

## 🔒 Security Best Practices

  * **Never commit secrets:** Add `.env` and `cdp_api_key.json` to your `.gitignore`.
  * **Use IP allowlists:** Restrict API access to your machine's IP address.
  * **Start small:** Test with minimal funds.
  * **Use read-only keys first:** Ensure safe data retrieval before enabling trading.
  * **Rotate keys regularly.**
  * **Store secrets securely:** Use environment variables or secret managers.

-----

## 🛠️ Troubleshooting

| Error Message | Possible Fixes |
| :--- | :--- |
| "Wallet Secret not configured" | Ensure `.env` contains `CDP_WALLET_SECRET`; verify the secret is correct. |
| "401 Unauthorized" | Check your IP allowlist (use `0.0.0.0/0` for testing); verify API key permissions; ensure `cdp_api_key.json` is in the correct location. |
| "python-dotenv could not parse statement" | Check for syntax errors in `.env`. Format must be `KEY=value` with no quotes or spaces around `=`. |

-----

## 🔗 Important Links

  * CDP Portal: `https://portal.cdp.coinbase.com/projects`
  * CDP Documentation: `https://docs.cdp.coinbase.com/`

-----

## ⚠️ Disclaimer

**This tool is for educational purposes only.**

  * Cryptocurrency trading carries significant risk.
  * Never invest more than you can afford to lose.
  * Past performance does not guarantee future results.
  * Always do your own research (DYOR).
  * **This is not financial advice.**

-----

## 📜 License

This project is licensed under the **MIT License**.

-----

## 💬 Support

  * For code issues: **Open an issue on GitHub.**
  * For CDP API questions: **Refer to the CDP Docs.**
  * For Coinbase account issues: **Contact Coinbase Support.**

<!-- end list -->

```

Would you like me to refine a specific section of this formatted Readme, such as the **Security Best Practices** or the **Troubleshooting** guide?
```
