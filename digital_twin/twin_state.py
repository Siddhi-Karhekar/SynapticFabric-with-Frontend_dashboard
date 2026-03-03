import random

def get_digital_twin_state():

    # simulated physics outputs
    predicted_temp = round(310 + random.uniform(-2, 2), 2)
    vibration_index = round(random.uniform(0.2, 0.9), 2)
    anomaly_score = round(random.uniform(0, 1), 2)

    twin_context = f"""
Predicted Process Temperature: {predicted_temp} K
Vibration Index: {vibration_index}
Anomaly Score: {anomaly_score}
"""

    return twin_context