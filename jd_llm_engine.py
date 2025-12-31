from sentence_transformers import SentenceTransformer, util
from skills_config import SKILLS

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_skills_from_jd(jd_text, threshold=0.45):
    """
    Extract skills from JD using semantic similarity.
    Returns a clean list of relevant skills.
    """

    jd_text = jd_text.lower()

    jd_embedding = model.encode(jd_text)
    skill_embeddings = model.encode(SKILLS)

    extracted_skills = []

    for skill, emb in zip(SKILLS, skill_embeddings):
        similarity = util.cos_sim(jd_embedding, emb).item()
        if similarity >= threshold:
            extracted_skills.append(skill)

    return sorted(set(extracted_skills))
