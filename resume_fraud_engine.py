# resume_fraud_engine.py

import re
from collections import Counter
from hiring_decision_engine import make_hiring_decision

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

# Skills that usually require proof
ADVANCED_SKILLS = [
    "machine learning", "deep learning",
    "aws", "kubernetes", "blockchain",
    "devops", "data science"
]

# =========================
# FRAUD DETECTION ENGINE
# =========================
def analyze_resume_fraud(resume_text, extracted_skills):
    text = resume_text.lower()

    fraud_score = 0
    red_flags = []

    # ---------------------------------
    # 1️⃣ Skill stuffing detection
    # ---------------------------------
    if len(extracted_skills) > 25:
        fraud_score += 15
        red_flags.append("Excessive number of skills listed")

    # ---------------------------------
    # 2️⃣ Buzzword inflation
    # ---------------------------------
    buzz_count = sum(1 for word in BUZZWORDS if word in text)
    if buzz_count >= 3:
        fraud_score += 10
        red_flags.append("Heavy use of buzzwords without evidence")

    # ---------------------------------
    # 3️⃣ Weak vs strong verb ratio
    # ---------------------------------
    weak_count = sum(1 for v in WEAK_VERBS if v in text)
    strong_count = sum(1 for v in STRONG_VERBS if v in text)

    if weak_count > strong_count:
        fraud_score += 10
        red_flags.append("Responsibilities described without action verbs")

    # ---------------------------------
    # 4️⃣ Advanced skill proof check
    # ---------------------------------
    for skill in ADVANCED_SKILLS:
        if skill in extracted_skills:
            # look for project evidence
            evidence = any(
                kw in text for kw in [
                    "project", "implemented", "built",
                    "deployed", "architecture", "pipeline"
                ]
            )
            if not evidence:
                fraud_score += 8
                red_flags.append(f"Advanced skill '{skill}' lacks evidence")

    # ---------------------------------
    # 5️⃣ Repetitive template detection
    # ---------------------------------
    repeated_phrases = Counter(re.findall(r"\b\w+\b", text))
    if any(count > 25 for count in repeated_phrases.values()):
        fraud_score += 7
        red_flags.append("Resume appears template-based or repetitive")

    # ---------------------------------
    # Final Verdict
    # ---------------------------------
    if fraud_score >= 30:
        verdict = "HIGH RISK"
    elif fraud_score >= 15:
        verdict = "MEDIUM RISK"
    else:
        verdict = "LOW RISK"

    return {
        "fraud_score": fraud_score,
        "risk_level": verdict,
        "red_flags": red_flags
    }

res = analyze_resume_fraud("sample text about projects and AWS", ["aws", "python"])
print(make_hiring_decision(60, 0, 0, 0, 1.0, 10, fraud_result=res))
