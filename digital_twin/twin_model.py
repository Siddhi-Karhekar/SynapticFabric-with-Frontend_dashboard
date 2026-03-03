def simulate_machine_state(temp, torque, tool_wear):

    friction_factor = 1 + (tool_wear / 100)
    heat_generation = torque * friction_factor * 0.05

    predicted_temp = temp + heat_generation
    vibration_index = torque * friction_factor * 0.02

    anomaly_score = (
        predicted_temp * 0.4 +
        vibration_index * 0.4 +
        tool_wear * 0.2
    )

    # ---------------------------
    # Health Classification
    # ---------------------------
    if anomaly_score < 80:
        health_status = "NORMAL"
    elif anomaly_score < 120:
        health_status = "WARNING"
    else:
        health_status = "CRITICAL"

    return {
        "predicted_temperature": predicted_temp,
        "vibration_index": vibration_index,
        "anomaly_score": anomaly_score,
        "health_status": health_status
    }