from statistics import mean


def compute_realtime_analytics(machines):

    if not machines:
        return {}

    failure_probs = [m.get("failure_probability", 0) for m in machines]
    vibrations = [m.get("vibration_index", 0) for m in machines]

    plant_health = 1 - mean(failure_probs)

    most_unstable = max(
        machines,
        key=lambda m: m.get("vibration_index", 0)
    )

    machines_needing_attention = [
        m["machine_id"]
        for m in machines
        if m.get("failure_probability", 0) > 0.6
    ]

    return {
        "plant_health_score": round(plant_health, 3),
        "most_unstable_machine": most_unstable["machine_id"],
        "machines_needing_attention": machines_needing_attention
    }