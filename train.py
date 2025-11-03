# train.py
import os
from ml_pipeline import get_crypto_data, add_indicators, train_model, save_model

def main():
    os.makedirs("models", exist_ok=True)
    coin = "bitcoin"
    days = 180
    print(f"Fetching {coin} {days}d")
    df = get_crypto_data(coin, days=days)
    df = add_indicators(df)
    model, acc, X_test, y_test = train_model(df)
    print("Test accuracy:", acc)
    save_model(model, path="models/rf_model.joblib")
    print("Saved model to models/rf_model.joblib")

if __name__ == "__main__":
    main()
