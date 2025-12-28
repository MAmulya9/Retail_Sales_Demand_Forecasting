import numpy as np
import pandas as pd

def predict_ma(config, store_id, dates):
    if store_id not in config:
        raise KeyError(
            f"Moving Average model not available for Store {store_id}"
        )

    window = config[store_id]["window"]
    history = list(config[store_id]["last_values"])
    preds = []

    for _ in dates:
        pred = sum(history[-window:]) / window
        preds.append(pred)
        history.append(pred)

    return preds


def predict_exp(models, store_id, steps):
    return models[store_id].forecast(steps)

import pandas as pd

def predict_lgbm(models, store_id, X):
    model = models[store_id]
    booster = model.booster_

    # Ensure correct column order
    feature_names = booster.feature_name()
    X = X[feature_names].copy()

    # Convert ALL non-numeric columns to numeric codes
    for col in X.columns:
        if not np.issubdtype(X[col].dtype, np.number):
            X[col] = X[col].astype("category").cat.codes

    # Replace NaNs (LightGBM-safe)
    X = X.fillna(0)

    # 🔥 CRITICAL PART: convert to NumPy and call Booster directly
    X_np = X.to_numpy(dtype=np.float32)

    return booster.predict(X_np)



def predict_lstm(model, scaler, last_seq, steps):
    preds = []
    seq = last_seq.copy()

    for _ in range(steps):
        scaled = scaler.transform(seq.reshape(-1, 1))
        pred = model.predict(
            scaled.reshape(1, -1, 1),
            verbose=0
        )[0][0]
        preds.append(pred)
        seq = np.append(seq[1:], pred)

    return preds
