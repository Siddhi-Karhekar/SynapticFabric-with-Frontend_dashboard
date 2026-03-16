import random

# ==========================================
# MACHINE MEMORY
# ==========================================

MACHINE_MEMORY = {
    "M_1": {"tool_wear": 0.2, "vibration_index": 0.4, "anomaly_score": 0.05},
    "M_2": {"tool_wear": 0.2, "vibration_index": 0.4, "anomaly_score": 0.05},
    "M_3": {"tool_wear": 0.2, "vibration_index": 0.4, "anomaly_score": 0.05},
}


# ==========================================
# DIGITAL TWIN SIMULATOR
# ==========================================

def run_digital_twin():

    machines = []

    for machine_id, state in MACHINE_MEMORY.items():

        # gradual degradation
        state["tool_wear"] += random.uniform(0.0005, 0.002)
        state["vibration_index"] += random.uniform(0.0005, 0.002)
        state["anomaly_score"] += random.uniform(0.0005, 0.002)

        # clamp values
        state["tool_wear"] = min(state["tool_wear"], 1)
        state["vibration_index"] = min(state["vibration_index"], 1.5)
        state["anomaly_score"] = min(state["anomaly_score"], 1)

        temperature = 295 + state["vibration_index"] * 10 + random.uniform(-1, 1)
        torque = random.uniform(38, 48)

        machines.append({
            "machine_id": machine_id,
            "temperature": round(temperature, 2),
            "torque": round(torque, 2),
            "tool_wear": round(state["tool_wear"], 3),
            "vibration_index": round(state["vibration_index"], 3),
            "anomaly_score": round(state["anomaly_score"], 3),
        })

    return machines