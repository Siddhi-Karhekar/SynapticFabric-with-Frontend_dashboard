from sklearn.ensemble import IsolationForest
import numpy as np

model = IsolationForest(contamination=0.1)


def train_anomaly_model():
    # dummy training (you can later use real data)
    data = np.random.rand(1000, 4)
    model.fit(data)


def detect_anomaly(machine):

    X = [[
        machine.get("temperature", 295),
        machine.get("torque", 40),
        machine.get("tool_wear", 0.1),
        machine.get("vibration_index", 0.2)
    ]]

    score = model.decision_function(X)[0]

    return round(score, 3)