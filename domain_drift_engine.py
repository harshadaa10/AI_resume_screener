# domain_drift_engine.py

TRANSFERABLE_SKILLS = [
    "project management",
    "leadership",
    "communication",
    "documentation",
    "data analysis",
    "problem solving",
    "compliance",
    "stakeholder management",
    "reporting"
]

DOMAIN_RELATIONSHIP_GRAPH = {
    "HR": ["Management", "Consultant", "Education", "Public-Relations"],
    "Information-Technology": ["Engineering", "Business-Analyst", "Designer", "Digital-Media"],
    "Engineering": ["Information-Technology", "Construction", "Architect"],
    "Construction": ["Engineering", "Architect"],
    "Architect": ["Construction", "Engineering", "Designer"],
    "Finance": ["Banking", "Accountant", "Management"],
    "Accountant": ["Finance", "Banking"],
    "Banking": ["Finance", "Accountant", "Sales"],
    "Sales": ["Marketing", "Consultant", "Management", "Public-Relations"],
    "Consultant": ["Management", "Business-Analyst", "Sales"],
    "Designer": ["Digital-Media", "Architect", "Information-Technology"],
    "Digital-Media": ["Designer", "Sales", "Public-Relations"],
    "Business-Analyst": ["Management", "Consultant", "Information-Technology"],
    "Education": ["HR", "Management"],
    "Public-Relations": ["Sales", "Digital-Media", "Management"],
    "Agriculture": ["Management"],
    "BPO": ["Sales", "HR"],
    "Chef": ["Hospitality"],
    "Fitness": ["Health"],
    "Arts": ["Designer"],
    "Aviation": ["Engineering", "Management"],
    "Apparel": ["Designer", "Management"]
}


def analyze_domain_drift(jd_domain, resume_domain, resume_skills):
    resume_skills = [s.lower() for s in resume_skills]

    # ========================
    # 1️⃣ Drift Classification
    # ========================
    if jd_domain == resume_domain:
        drift_type = "None"
        drift_penalty = 0
        explanation = "Exact domain match"

    elif resume_domain in DOMAIN_RELATIONSHIP_GRAPH.get(jd_domain, []):
        drift_type = "Soft"
        drift_penalty = -5
        explanation = "Closely related domain"

    else:
        drift_type = "Hard"
        drift_penalty = -15
        explanation = "Unrelated domain"

    # ==========================
    # 2️⃣ Transferable Skill Bonus
    # ==========================
    transferable_hits = [
        skill for skill in TRANSFERABLE_SKILLS
        if skill in resume_skills
    ]

    transfer_bonus = min(len(transferable_hits) * 3, 10)

    return {
        "drift_type": drift_type,
        "drift_penalty": drift_penalty,
        "transfer_bonus": transfer_bonus,
        "transferable_skills": transferable_hits,
        "explanation": explanation
    }
