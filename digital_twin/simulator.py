# ==========================================================
# SYNAPTICFABRIC — DIGITAL TWIN SIMULATOR (FIXED)
# ==========================================================

import random


def run_digital_twin():
    """
    Generates FLAT machine schema expected by:
    - Machine Analyzer
    - WebSocket
    - React Dashboard
    """

    machines = []

    for i in range(1, 4):

        temperature = random.uniform(290, 320)
        vibration = random.uniform(0.3, 1.2)
        anomaly = random.uniform(0, 1)   # IMPORTANT: normalized 0–1

        machines.append({
            # -----------------------------
            # REQUIRED ROOT FIELDS
            # -----------------------------
            "machine_id": f"M_{i}",

            "temperature": round(temperature, 2),
            "torque": round(random.uniform(30, 50), 2),

            # convert wear into percentage-like scale
            "tool_wear": round(random.uniform(0.2, 0.9), 3),

            "vibration_index": round(vibration, 3),

            # AI scoring input
            "anomaly_score": round(anomaly, 3),
        })

    return machines