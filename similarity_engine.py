from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(resume_embedding, jd_embedding):
    """
    Compute cosine similarity between resume and JD embeddings
    """
    # Ensure 2D arrays
    resume_embedding = resume_embedding.reshape(1, -1)
    jd_embedding = jd_embedding.reshape(1, -1)

    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    return score
