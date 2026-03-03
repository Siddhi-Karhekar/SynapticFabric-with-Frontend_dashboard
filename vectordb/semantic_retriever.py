import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = Path("vectordb/faiss_index.bin")
META_PATH = Path("vectordb/metadata.pkl")

index = faiss.read_index(str(INDEX_PATH))

with open(META_PATH, "rb") as f:
    texts = pickle.load(f)


def retrieve_similar_context(query, k=3):

    q_emb = MODEL.encode([query])

    distances, indices = index.search(
        np.array(q_emb).astype("float32"), k
    )

    results = [texts[i] for i in indices[0]]

    return "\n".join(results)