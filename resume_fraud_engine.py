# resume_fraud_engine.py

import re
from collections import Counter

# =========================
# 🚩 RED FLAG CONFIG
# =========================
BUZZWORDS = [
    "expert", "proficient", "highly skilled", "guru",
    "seasoned", "world class", "best in class"
]

WEAK_VERBS = [
    "worked on", "responsible for", "involved in",
    "assisted with", "helped"
]

STRONG_VERBS = [
    "designed", "implemented", "optimized",
    "built", "automated", "deployed", "led"
]

ADVANCED_SKILLS = [
    "machine learning", "deep learning",
    "aws", "kubernetes", "blockchain",
    "devops", "data science"
]

# =========================
# 🚨 FRAUD / INFLATION DETECTOR
# =========================
def detect_resume_fraud(resume_text: str, jd_text: str):
    """
    Detects resume inflation, buzzword stuffing, and weak claims.
    Returns penalty score and explanation flags.
    """

    text = resume_text.lower()

    fraud_penalty = 0
    fraud_flags = []

    # ---------------------------------
    # 1️⃣ Buzzword inflation
    # ---------------------------------
    buzz_count = sum(1 for word in BUZZWORDS if word in text)
    if buzz_count >= 3:
        fraud_penalty += 8
        fraud_flags.append("Excessive buzzword usage")

    # ---------------------------------
    # 2️⃣ Weak vs strong action verbs
    # ---------------------------------
    weak_count = sum(1 for v in WEAK_VERBS if v in text)
    strong_count = sum(1 for v in STRONG_VERBS if v in text)

    if weak_count > strong_count:
        fraud_penalty += 6
        fraud_flags.append("Responsibilities lack strong action verbs")

    # ---------------------------------
    # 3️⃣ Advanced skill evidence check
    # ---------------------------------
    for skill in ADVANCED_SKILLS:
        if skill in text:
            has_evidence = any(
                kw in text for kw in [
                    "project", "implemented", "built",
                    "deployed", "architecture", "pipeline"
                ]
            )
            if not has_evidence:
                fraud_penalty += 5
                fraud_flags.append(f"Advanced skill '{skill}' lacks evidence")

    # ---------------------------------
    # 4️⃣ Repetitive / template detection
    # ---------------------------------
    words = re.findall(r"\b\w+\b", text)
    freq = Counter(words)

    if any(count > 30 for count in freq.values()):
        fraud_penalty += 6
        fraud_flags.append("Resume appears template-based or repetitive")

    # ---------------------------------
    # Cap penalty (safety)
    # ---------------------------------
    fraud_penalty = min(fraud_penalty, 25)

    return {
        "penalty": fraud_penalty,
        "flags": fraud_flags
    }
