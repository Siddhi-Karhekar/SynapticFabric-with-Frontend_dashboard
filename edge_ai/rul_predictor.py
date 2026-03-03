def predict_rul(tool_wear, anomaly_score):

    # simple engineering heuristic model
    base_life = 250  # minutes remaining baseline

    wear_penalty = tool_wear * 1.2
    anomaly_penalty = anomaly_score * 80

    rul = max(0, base_life - wear_penalty - anomaly_penalty)

    return f"Estimated Remaining Useful Life: {round(rul,1)} minutes"