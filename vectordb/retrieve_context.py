# vectordb/retrieve_context.py

from vectordb.data_loader import load_machine_data
import pandas as pd
from pathlib import Path


# ---------------------------------------------------
# DATA PATH (robust project-safe path)
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "predictive_maintenance_dataset_expanded.csv"


# ---------------------------------------------------
# RAG CONTEXT FOR CHATBOT
# ---------------------------------------------------

def get_machine_context():
    """
    Returns latest machine info formatted
    for RAG chatbot context.
    """

    df = load_machine_data()
    latest = df.iloc[-1]

    context = f"""
Machine ID: {latest['machine_id']}
Air Temp (K): {latest['air_temperature_K']}
Process Temp (K): {latest['process_temperature_K']}
Torque (Nm): {latest['torque_Nm']}
Tool Wear (min): {latest['tool_wear_min']}
Machine Failure: {latest['machine_failure']}
"""

    return context


# ---------------------------------------------------
# DIGITAL TWIN INPUT STATE
# ---------------------------------------------------

def get_latest_machine_state():
    """
    Returns latest machine sensor values
    for Digital Twin simulation.
    """

    df = pd.read_csv(DATA_PATH)

    latest = df.iloc[-1]

    return {
        "machine_id": str(latest["machine_id"]),
        "temperature": float(latest["air_temperature_K"]),
        "torque": float(latest["torque_Nm"]),
        "tool_wear": float(latest["tool_wear_min"]),
    }