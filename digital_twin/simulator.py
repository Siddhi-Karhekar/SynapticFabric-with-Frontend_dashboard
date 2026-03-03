# ==========================================================
# SYNAPTICFABRIC — BALANCED INDUSTRIAL DIGITAL TWIN
# ==========================================================

import random

# ----------------------------------------------------------
# STATE MEMORY (PERSISTENT)
# ----------------------------------------------------------

MACHINE_MEMORY = {
    f"M_{i}": {
        "temperature": random.uniform(295, 305),
        "torque": random.uniform(35, 45),
        "tool_wear": random.uniform(0.15, 0.25),
        "vibration_index": random.uniform(0.3, 0.5),
        "anomaly_score": random.uniform(0.05, 0.15),
    }
    for i in range(1, 4)
}


# ----------------------------------------------------------
# SIMULATION STEP
# ----------------------------------------------------------

def run_digital_twin():
    machines = []

    for machine_id, state in MACHINE_MEMORY.items():

        # --- Temperature smooth oscillation
        state["temperature"] += random.uniform(-0.5, 0.5)

        # --- Torque small noise
        state["torque"] += random.uniform(-0.2, 0.2)

        # --- Wear increases VERY slowly
        state["tool_wear"] += random.uniform(0.0002, 0.0008)

        # --- Vibration reacts to wear but stabilizes
        wear_factor = state["tool_wear"] * 0.5
        state["vibration_index"] += random.uniform(-0.02, 0.02)
        state["vibration_index"] += wear_factor * 0.01

        # --- Anomaly grows only if vibration sustained high
        if state["vibration_index"] > 1.1:
            state["anomaly_score"] += random.uniform(0.005, 0.015)
        else:
            state["anomaly_score"] -= random.uniform(0.01, 0.02)

        # Clamp ranges
        state["temperature"] = max(290, min(320, state["temperature"]))
        state["torque"] = max(30, min(50, state["torque"]))
        state["tool_wear"] = max(0, min(0.9, state["tool_wear"]))
        state["vibration_index"] = max(0.3, min(1.3, state["vibration_index"]))
        state["anomaly_score"] = max(0, min(1, state["anomaly_score"]))

        machines.append({
            "machine_id": machine_id,
            "temperature": round(state["temperature"], 2),
            "torque": round(state["torque"], 2),
            "tool_wear": round(state["tool_wear"], 3),
            "vibration_index": round(state["vibration_index"], 3),
            "anomaly_score": round(state["anomaly_score"], 3),
        })

    return machines
    