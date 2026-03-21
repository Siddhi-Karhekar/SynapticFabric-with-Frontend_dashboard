import pandas as pd
from xgboost import XGBRegressor
import joblib
import os

MODEL_PATH = "ml_models/failure_model.pkl"


# ==========================================
# 🚀 TRAIN MODEL (REGRESSION)
# ==========================================
def train_model(data_path):

    print("📂 Loading dataset:", data_path)

    df = pd.read_csv(data_path)

    print("✅ Columns:", df.columns.tolist())

    # ======================================
    # FEATURES (MATCH YOUR SYSTEM)
    # ======================================
    X = df[[
        "temperature",
        "torque",
        "tool_wear",
        "vibration_index"
    ]]

    # ======================================
    # TARGET → anomaly_score
    # ======================================
    y = df["anomaly_score"]

    # ======================================
    # MODEL (REGRESSOR)
    # ======================================
    model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05
    )

    model.fit(X, y)

    # ======================================
    # SAVE MODEL
    # ======================================
    os.makedirs("ml_models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("✅ Model trained & saved at:", MODEL_PATH)


# ==========================================
# 🤖 PREDICT FAILURE (USED IN ANALYZER)
# ==========================================
def predict_failure(machine):

    if not os.path.exists(MODEL_PATH):
        raise Exception("Model not trained yet")

    model = joblib.load(MODEL_PATH)

    X = pd.DataFrame([{
        "temperature": machine.get("temperature", 295),
        "torque": machine.get("torque", 40),
        "tool_wear": machine.get("tool_wear", 0.1),
        "vibration_index": machine.get("vibration_index", 0.2)
    }])

    prediction = model.predict(X)[0]

    # clamp between 0–1
    prediction = max(0, min(prediction, 1))

    return round(float(prediction), 3)