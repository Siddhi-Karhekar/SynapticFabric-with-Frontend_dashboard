from digital_twin.simulator import run_digital_twin

def get_twin_context():

    twin_output = run_digital_twin()

    context = f"""
    Digital Twin Simulation Results:

    Predicted Temperature: {twin_output['simulated_state']['predicted_temperature']}
    Vibration Index: {twin_output['simulated_state']['vibration_index']}
    Anomaly Score: {twin_output['simulated_state']['anomaly_score']}
    """

    return context