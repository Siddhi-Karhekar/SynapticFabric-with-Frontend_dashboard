import os
print("FILES IN DATA:", os.listdir("data"))

from failure_model import train_model

train_model("data/predictive_maintenance_dataset_expanded.csv")