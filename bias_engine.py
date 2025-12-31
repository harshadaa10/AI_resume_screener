import re

# ==========================
# BIAS INDICATORS
# ==========================

COLLEGE_KEYWORDS = [
    "iit", "iim", "nit", "bits", "mit", "stanford",
    "harvard", "oxford", "cambridge"
]

GENDER_TERMS = [
    "he", "she", "his", "her", "him", "hers"
]

RELIGION_CASTE_TERMS = [
    "hindu", "muslim", "christian", "sikh",
    "brahmin", "sc", "st", "obc"
]


# ==========================
# MAIN FUNCTION
# ==========================
def analyze_bias(resume_text):
    """
    Detects bias-related content.
    Returns:
    {
        "bias_flags": list[str],
        "bias_penalty": int
    }
    """

    text = resume_text.lower()
    flags = []
    penalty = 0

    # --------------------------
    # 1️⃣ College Prestige Bias
    # --------------------------
    for college in COLLEGE_KEYWORDS:
        if college in text:
            flags.append("College prestige mention ignored")
            penalty += 0  # NO SCORE IMPACT
            break

    # --------------------------
    # 2️⃣ Gender Neutrality
    # --------------------------
    for term in GENDER_TERMS:
        if re.search(rf"\b{term}\b", text):
            flags.append("Gendered language detected and ignored")
            penalty += 0
            break

    # --------------------------
    # 3️⃣ Religion / Caste
    # --------------------------
    for term in RELIGION_CASTE_TERMS:
        if term in text:
            flags.append("Sensitive personal attribute ignored")
            penalty += 0
            break

    return {
        "bias_flags": flags,
        "bias_penalty": penalty
    }
