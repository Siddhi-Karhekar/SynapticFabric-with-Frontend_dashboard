def generate_feature_explanation():

    # simulated contribution scores
    contributions = {
        "Tool Wear": 0.42,
        "Process Temperature": 0.31,
        "Vibration Index": 0.18,
        "Torque Variation": 0.09,
    }

    explanation = "\n".join(
        [f"{k}: {int(v*100)}%" for k, v in contributions.items()]
    )

    return f"""
FEATURE CONTRIBUTION ANALYSIS:
{explanation}
"""