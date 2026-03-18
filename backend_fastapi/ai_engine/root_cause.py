def analyze_root_cause(machine):

    mid = machine["machine_id"]
    temp = machine["temperature"]
    vib = machine["vibration_index"]
    wear = machine["tool_wear"]
    torque = machine["torque"]

    causes = []

    # ==========================================
    # 🔥 GLOBAL FAILURE STAGES
    # ==========================================

    if wear > 0.85:
        causes.append({
            "issue": "Tool failure imminent",
            "confidence": wear,
            "reason": f"Tool wear {round(wear*100,1)}%"
        })

    elif wear > 0.6:
        causes.append({
            "issue": "Tool degradation",
            "confidence": wear,
            "reason": "Wear increasing"
        })

    # ==========================================
    # MACHINE SPECIFIC
    # ==========================================

    if mid == "M_1":
        if vib > 0.8:
            causes.append({
                "issue": "Bearing failure",
                "confidence": vib,
                "reason": "Severe vibration"
            })
        elif vib > 0.6:
            causes.append({
                "issue": "Spindle imbalance",
                "confidence": vib,
                "reason": "Moderate vibration"
            })

    elif mid == "M_2":
        if temp > 305:
            causes.append({
                "issue": "Cooling failure",
                "confidence": 0.9,
                "reason": f"Temp {round(temp,1)}°C"
            })
        elif temp > 300:
            causes.append({
                "issue": "Heat buildup",
                "confidence": 0.6,
                "reason": "Friction rising"
            })

    elif mid == "M_3":
        if torque > 55:
            causes.append({
                "issue": "Cutting overload",
                "confidence": 0.9,
                "reason": "High torque"
            })
        elif torque > 45:
            causes.append({
                "issue": "Cutting resistance",
                "confidence": 0.6,
                "reason": "Torque rising"
            })

    # ❌ REMOVE FALLBACK (IMPORTANT)

    return sorted(causes, key=lambda x: x["confidence"], reverse=True)