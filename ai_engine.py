from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    """
    Convert text to normalized numpy array embedding for cosine similarity.
    """
    if not text.strip():
        text = " "  # avoid empty string

    embedding = model.encode(
        text,
        convert_to_numpy=True,      # ensures numpy array
        normalize_embeddings=True   # ensures embeddings are unit vectors
    )

    # Debug: check embedding
    print("Embedding shape:", embedding.shape)
    return embedding
