from digital_twin.simulator import run_digital_twin


def get_twin_context():
    """
    Converts Digital Twin output into
    LLM-friendly engineering context.
    """

    twin_output = run_digital_twin()

    real = twin_output["real_state"]
    sim = twin_output["simulated_state"]

    context = f"""
Digital Twin Analysis:

Machine ID: {real['machine_id']}
Current Temperature: {real['temperature']:.2f} K
Torque: {real['torque']:.2f} Nm
Tool Wear: {real['tool_wear']:.2f} min

Predicted Temperature: {sim['predicted_temperature']:.2f} K
Vibration Index: {sim['vibration_index']:.2f}
Anomaly Score: {sim['anomaly_score']:.2f}

Machine Health Status: {sim['health_status']}
"""

    return context