# app.py
import streamlit as st
from ml_pipeline import (
    get_crypto_data,
    add_indicators,
    train_model,
    predict_latest,
)
import pandas as pd

st.set_page_config(page_title="CryptoInsightAI", layout="wide")
st.title("🚀 CryptoInsightAI — ML-Powered Crypto Signals (MVP)")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Settings")
    coin = st.selectbox("Choose coin (CoinGecko id)", ["bitcoin", "ethereum", "solana", "cardano", "ripple"])
    days = st.slider("History (days)", min_value=30, max_value=365, value=90, step=30)
    retrain = st.button("Retrain model (use cached by default)")

with col2:
    st.header("Live preview")
    st.write("This small demo trains a RandomForest to predict whether the next time-step price will go up or down.")

@st.cache_data(ttl=60 * 15)
def cached_get_data(coin_id, days):
    return get_crypto_data(coin_id, days=days)

data = cached_get_data(coin, days)
if data is None or data.empty:
    st.error("Failed to load data. Check your internet connection or CoinGecko API limits.")
    st.stop()

data = add_indicators(data)

# Train model (on-the-fly)
model, acc, X_test, y_test = train_model(data)

st.metric("Model accuracy (test)", f"{acc:.2%}")

# show latest signal
pred, proba = predict_latest(model, data)
signal = "BUY 🚀" if pred == 1 else "SELL ⚠️"
confidence = f"{proba:.1%}"

st.subheader(f"Current signal for {coin.upper()}: {signal} (confidence {confidence})")

# Show price chart + indicators
st.subheader("Price Chart")
chart_df = data.set_index("timestamp")[["price", "sma_10", "sma_30"]].dropna()
st.line_chart(chart_df)

# Show feature table (latest row)
st.subheader("Latest features")
latest = data.iloc[-1][["price", "rsi", "sma_10", "sma_30", "momentum"]]
st.table(latest.to_frame("value"))

# Show dataset preview and evaluation details
with st.expander("Dataset & Evaluation details"):
    st.write("Dataset (last 10 rows):")
    st.dataframe(data.tail(10))

    st.write("Test set class distribution:")
    st.write(pd.Series(y_test).value_counts())

    st.write("Feature columns used:")
    st.write(list(X_test.columns))
