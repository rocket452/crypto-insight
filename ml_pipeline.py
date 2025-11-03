# ml_pipeline.py
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import io

# technical analysis
import ta

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

def get_crypto_data(coin_id="bitcoin", days=90):
    """
    Fetch market_chart from CoinGecko.
    Returns DataFrame with columns: timestamp (pd.Timestamp), price (float)
    """
    url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")
        prices = prices.sort_values("timestamp").reset_index(drop=True)
        return prices
    except Exception as e:
        print("Error fetching data:", e)
        return pd.DataFrame()

def add_indicators(df):
    """
    Add RSI, SMA indicators and simple momentum feature.
    Assumes df has 'price' and 'timestamp'
    """
    df = df.copy()
    df["price"] = df["price"].astype(float)
    # RSI (14)
    try:
        rsi = ta.momentum.RSIIndicator(df["price"], window=14)
        df["rsi"] = rsi.rsi()
    except Exception:
        df["rsi"] = np.nan

    # SMA short/long
    try:
        df["sma_10"] = ta.trend.SMAIndicator(df["price"], window=10).sma_indicator()
        df["sma_30"] = ta.trend.SMAIndicator(df["price"], window=30).sma_indicator()
    except Exception:
        df["sma_10"] = np.nan
        df["sma_30"] = np.nan

    # momentum: pct change over 3 periods
    df["momentum"] = df["price"].pct_change(periods=3)

    # drop NA rows
    df = df.dropna().reset_index(drop=True)
    return df

def prepare_features(df):
    """
    Prepares X (features) and y (target). Target: whether next price is higher (1) or not (0)
    """
    df = df.copy()
    df["target"] = (df["price"].shift(-1) > df["price"]).astype(int)
    df = df.dropna().reset_index(drop=True)
    feature_cols = ["rsi", "sma_10", "sma_30", "momentum"]
    X = df[feature_cols]
    y = df["target"].astype(int)
    return X, y

def train_model(df, test_size=0.2, random_state=42):
    """
    Train a RandomForestClassifier on the prepared features.
    Returns model, accuracy, X_test, y_test
    """
    X, y = prepare_features(df)
    if len(X) < 50:
        # Not enough data to train
        model = RandomForestClassifier(n_estimators=10, random_state=random_state)
        model.fit(X, y)  # may be trivial
        return model, 0.0, X, y

    # avoid shuffling time-series data for split
    split_idx = int(len(X) * (1 - test_size))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    return model, acc, X_test, y_test

def predict_latest(model, df):
    """
    Predict last row's up/down and return label and probability for 'up' class.
    """
    X, y = prepare_features(df)
    latest = X.iloc[-1].values.reshape(1, -1)
    pred = model.predict(latest)[0]
    proba = None
    try:
        proba = model.predict_proba(latest)[0][1]
    except Exception:
        # model may not implement predict_proba
        proba = 0.0
    return int(pred), float(proba)

def save_model(model, path="models/rf_model.joblib"):
    joblib.dump(model, path)

def load_model(path="models/rf_model.joblib"):
    return joblib.load(path)
