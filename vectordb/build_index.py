import faiss
import numpy as np
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
from vectordb.data_loader import load_machine_data

# embedding model
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = Path("vectordb/faiss_index.bin")
META_PATH = Path("vectordb/metadata.pkl")


def row_to_text(row):
    return (
        f"Machine {row['machine_id']} "
        f"AirTemp {row['air_temperature_K']} "
        f"ProcessTemp {row['process_temperature_K']} "
        f"Torque {row['torque_Nm']} "
        f"ToolWear {row['tool_wear_min']} "
        f"Failure {row['machine_failure']}"
    )


def build_index():

    df = load_machine_data()

    texts = df.apply(row_to_text, axis=1).tolist()

    print("Creating embeddings...")
    embeddings = MODEL.encode(texts)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, str(INDEX_PATH))

    with open(META_PATH, "wb") as f:
        pickle.dump(texts, f)

    print("✅ Vector index built successfully!")


if __name__ == "__main__":
    build_index()