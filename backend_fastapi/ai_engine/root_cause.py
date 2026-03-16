def analyze_root_cause(machine):

    causes = []

    temperature = machine.get("temperature", 0)
    vibration = machine.get("vibration_index", 0)
    tool_wear = machine.get("tool_wear", 0)
    torque = machine.get("torque", 0)

    # Temperature related faults
    if temperature > 85:
        causes.append("Cooling system degradation")

    # Vibration related faults
    if vibration > 0.7:
        causes.append("Bearing wear or spindle imbalance")

    # Tool wear
    if tool_wear > 0.8:
        causes.append("Cutting tool nearing end of life")

    # Torque overload
    if torque > 60:
        causes.append("Mechanical overload")

    if not causes:
        causes.append("No abnormal mechanical pattern detected")

    return causes