# ==========================================================
# SYNAPTICFABRIC — REALISTIC DIGITAL TWIN SIMULATOR
# ==========================================================

import random


# ----------------------------------------------------------
# MACHINE STATE MEMORY
# ----------------------------------------------------------

MACHINE_MEMORY = {
    "M_1": {
        "tool_wear": 0.1,
        "vibration_index": 0.35,
        "anomaly_score": 0.05
    },
    "M_2": {
        "tool_wear": 0.12,
        "vibration_index": 0.36,
        "anomaly_score": 0.05
    },
    "M_3": {
        "tool_wear": 0.09,
        "vibration_index": 0.34,
        "anomaly_score": 0.04
    }
}


# ----------------------------------------------------------
# DIGITAL TWIN STEP
# ----------------------------------------------------------

def run_digital_twin():

    machines = []

    for machine_id, state in MACHINE_MEMORY.items():

        # --------------------------------------------------
        # SLOW DEGRADATION MODEL
        # --------------------------------------------------

        # tool wear increases slowly
        state["tool_wear"] += random.uniform(0.001, 0.004)

        # vibration reacts to wear
        state["vibration_index"] += random.uniform(0.001, 0.003)

        # anomaly grows slowly
        state["anomaly_score"] += random.uniform(0.002, 0.006)

        # --------------------------------------------------
        # CLAMP VALUES
        # --------------------------------------------------

        state["tool_wear"] = min(state["tool_wear"], 1)
        state["vibration_index"] = min(state["vibration_index"], 1.4)
        state["anomaly_score"] = min(state["anomaly_score"], 1)

        # --------------------------------------------------
        # TEMPERATURE MODEL
        # --------------------------------------------------

        temperature = (
            295 +
            state["vibration_index"] * 10 +
            random.uniform(-1.5, 1.5)
        )

        # --------------------------------------------------
        # TORQUE
        # --------------------------------------------------

        torque = random.uniform(38, 48)

        machines.append({
            "machine_id": machine_id,
            "temperature": round(temperature, 2),
            "torque": round(torque, 2),
            "tool_wear": round(state["tool_wear"], 3),
            "vibration_index": round(state["vibration_index"], 3),
            "anomaly_score": round(state["anomaly_score"], 3)
        })

    return machines