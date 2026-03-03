import pandas as pd
from pathlib import Path

# Get project root dynamically
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "predictive_maintenance_dataset_expanded.csv"

def load_machine_data():
    df = pd.read_csv(DATA_PATH)
    return df