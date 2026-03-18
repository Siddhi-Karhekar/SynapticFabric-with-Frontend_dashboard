# digital_twin/simulator.py

import random

# ==========================================
# MACHINE MEMORY (STATEFUL)
# ==========================================

MACHINE_MEMORY = {
    "M_1": {
        "tool_wear": 0.15,
        "vibration_index": 0.25,
        "temperature": 295,
        "torque": 40
    },
    "M_2": {
        "tool_wear": 0.10,
        "vibration_index": 0.20,
        "temperature": 295,
        "torque": 40
    },
    "M_3": {
        "tool_wear": 0.12,
        "vibration_index": 0.18,
        "temperature": 295,
        "torque": 42
    },
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))


# ==========================================
# MAIN DIGITAL TWIN
# ==========================================

def run_digital_twin():

    machines = []

    for machine_id, state in MACHINE_MEMORY.items():

        # ======================================
        # 🔵 BASE SLOW DEGRADATION (REALISTIC)
        # ======================================
        state["tool_wear"] += random.uniform(0.0005, 0.002)
        state["vibration_index"] += random.uniform(0.0003, 0.001)

        # ======================================
        # 🧠 MACHINE-SPECIFIC BEHAVIOR
        # ======================================

        # 🔵 CNC MILLING (M1)
        if machine_id == "M_1":
            # Higher vibration system
            state["vibration_index"] += random.uniform(0.001, 0.003)

            # Wear depends on vibration
            state["tool_wear"] += state["vibration_index"] * 0.002

            # Occasional instability spike
            if random.random() < 0.02:
                state["vibration_index"] += random.uniform(0.02, 0.05)

        # 🟡 CNC DRILLING (M2)
        elif machine_id == "M_2":
            # Heat accumulates slowly
            state["temperature"] += random.uniform(0.05, 0.15)

            # Cooling effect (stabilization)
            if state["temperature"] > 305:
                state["temperature"] -= random.uniform(0.1, 0.3)

            # Wear slower but steady
            state["tool_wear"] += 0.0008

        # 🟢 CNC LATHE (M3)
        elif machine_id == "M_3":
            # Torque-driven system
            state["torque"] = 40 + state["tool_wear"] * 25

            # Stable machine (slow degradation)
            state["tool_wear"] += random.uniform(0.0003, 0.001)

            # Occasional load spike
            if random.random() < 0.015:
                state["torque"] += random.uniform(3, 8)

        # ======================================
        # 🌡 GLOBAL TEMPERATURE MODEL
        # ======================================

        # small drift
        state["temperature"] += random.uniform(-0.05, 0.2)

        # stabilization (prevents runaway heat)
        if state["temperature"] > 300:
            state["temperature"] -= random.uniform(0.05, 0.15)

        # ======================================
        # 🔁 NATURAL RECOVERY (VERY IMPORTANT)
        # ======================================

        # vibration damping
        if random.random() < 0.1:
            state["vibration_index"] *= 0.98

        # slight thermal recovery
        if random.random() < 0.05:
            state["temperature"] -= random.uniform(0.1, 0.3)

        # ======================================
        # LIMITS (PHYSICAL CONSTRAINTS)
        # ======================================

        state["tool_wear"] = clamp(state["tool_wear"], 0, 1)
        state["vibration_index"] = clamp(state["vibration_index"], 0, 1)
        state["temperature"] = clamp(state["temperature"], 290, 320)
        state["torque"] = clamp(state["torque"], 35, 80)

        # ======================================
        # OUTPUT SNAPSHOT
        # ======================================

        machines.append({
            "machine_id": machine_id,
            "temperature": round(state["temperature"], 2),
            "torque": round(state["torque"], 2),
            "tool_wear": round(state["tool_wear"], 4),
            "vibration_index": round(state["vibration_index"], 4)
        })

    return machines