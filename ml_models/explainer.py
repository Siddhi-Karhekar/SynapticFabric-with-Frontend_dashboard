import shap
import joblib
import pandas as pd

MODEL_PATH = "ml_models/failure_model.pkl"

explainer = None
model = None


def load_explainer():
    global explainer, model

    if model is None:
        model = joblib.load(MODEL_PATH)
        explainer = shap.Explainer(model)


def explain_prediction(machine):

    load_explainer()

    X = pd.DataFrame([{
        "temperature": machine.get("temperature", 295),
        "torque": machine.get("torque", 40),
        "tool_wear": machine.get("tool_wear", 0.1),
        "vibration_index": machine.get("vibration_index", 0.2)
    }])

    shap_values = explainer(X)

    contributions = {}

    for i, col in enumerate(X.columns):
        contributions[col] = float(shap_values.values[0][i])

    return contributions