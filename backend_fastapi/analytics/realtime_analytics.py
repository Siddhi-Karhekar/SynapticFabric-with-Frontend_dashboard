def compute_realtime_analytics(machines):

    if not machines:
        return {}

    total = len(machines)

    # Plant health score
    avg_health = 0
    unstable_machine = None
    highest_anomaly = -1

    machines_needing_attention = []

    for m in machines:

        anomaly = m.get("anomaly_score", 0)

        avg_health += (1 - anomaly)

        if anomaly > highest_anomaly:
            highest_anomaly = anomaly
            unstable_machine = m.get("machine_id")

        if anomaly > 0.6:
            machines_needing_attention.append(m.get("machine_id"))

    plant_health_score = round((avg_health / total) * 100, 2)

    return {
        "plant_health_score": plant_health_score,
        "most_unstable_machine": unstable_machine,
        "total_machines": total,
        "machines_needing_attention": machines_needing_attention
    }