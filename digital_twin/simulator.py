# digital_twin/simulator.py

import random

# ==========================================
# MACHINE MEMORY (STATEFUL)
# ==========================================

MACHINE_MEMORY = {
    "M_1": {  # CNC MILLING (vibration-driven)
        "tool_wear": 0.12,
        "vibration_index": 0.30,
        "temperature": 295,
        "torque": 40
    },
    "M_2": {  # CNC DRILLING (heat-driven)
        "tool_wear": 0.08,
        "vibration_index": 0.18,
        "temperature": 295,
        "torque": 40
    },
    "M_3": {  # CNC LATHE (torque-driven)
        "tool_wear": 0.10,
        "vibration_index": 0.15,
        "temperature": 295,
        "torque": 42
    },
}


# ==========================================
# HELPER
# ==========================================

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))


# ==========================================
# DIGITAL TWIN ENGINE
# ==========================================

def run_digital_twin():

    machines = []

    for machine_id, state in MACHINE_MEMORY.items():

        # ======================================
        # 🔵 VERY LIGHT BASE DRIFT (COMMON)
        # ======================================
        state["tool_wear"] += random.uniform(0.0001, 0.0003)
        state["vibration_index"] += random.uniform(0.00005, 0.0002)

        # ======================================
        # 🔵 CNC MILLING (M1)
        # HIGH VIBRATION / UNSTABLE SYSTEM
        # ======================================
        if machine_id == "M_1":

            # vibration dominant
            state["vibration_index"] += random.uniform(0.002, 0.006)

            # vibration drives wear
            state["tool_wear"] += state["vibration_index"] * 0.003

            # occasional instability spikes
            if random.random() < 0.03:
                state["vibration_index"] += random.uniform(0.03, 0.08)

            # mild temperature effect
            state["temperature"] += random.uniform(-0.05, 0.1)

        # ======================================
        # 🟡 CNC DRILLING (M2)
        # HEAT-DRIVEN SYSTEM
        # ======================================
        elif machine_id == "M_2":

            # heat buildup
            state["temperature"] += random.uniform(0.1, 0.4)

            # heat accelerates wear
            if state["temperature"] > 300:
                state["tool_wear"] += 0.0015

            # cooling system behavior
            if state["temperature"] > 310:
                state["temperature"] -= random.uniform(0.3, 0.7)

            # very stable vibration
            state["vibration_index"] += random.uniform(0.0001, 0.0003)

        # ======================================
        # 🟢 CNC LATHE (M3)
        # TORQUE-DRIVEN SYSTEM
        # ======================================
        elif machine_id == "M_3":

            # torque depends on wear
            state["torque"] = 40 + state["tool_wear"] * 35

            # slow wear growth
            state["tool_wear"] += random.uniform(0.0003, 0.001)

            # occasional load spikes
            if random.random() < 0.02:
                state["torque"] += random.uniform(5, 10)

            # very stable system
            state["vibration_index"] *= 0.99
            state["temperature"] += random.uniform(-0.05, 0.1)

        # ======================================
        # 🌡 GLOBAL THERMAL STABILIZATION
        # ======================================

        # slight natural cooling
        if state["temperature"] > 300:
            state["temperature"] -= random.uniform(0.05, 0.2)

        # ======================================
        # 🔁 NATURAL RECOVERY EFFECTS
        # ======================================

        # vibration damping
        if random.random() < 0.1:
            state["vibration_index"] *= 0.97

        # slight cooling recovery
        if random.random() < 0.05:
            state["temperature"] -= random.uniform(0.1, 0.3)

        # ======================================
        # LIMITS (REALISTIC PHYSICS)
        # ======================================

        state["tool_wear"] = clamp(state["tool_wear"], 0, 1)
        state["vibration_index"] = clamp(state["vibration_index"], 0, 1)
        state["temperature"] = clamp(state["temperature"], 290, 330)
        state["torque"] = clamp(state["torque"], 35, 85)

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