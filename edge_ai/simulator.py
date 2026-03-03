import pandas as pd
import time

df = pd.read_csv("../data/predictive_maintenance_dataset_expanded.csv")

def stream():
    for _, row in df.iterrows():
        yield row.to_dict()
        time.sleep(2)