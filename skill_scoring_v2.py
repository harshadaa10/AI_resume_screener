# skill_scoring_v2.py

# Define skill importance
SKILL_WEIGHTS = {
    "core": 5,         # must-have
    "supporting": 3,   # nice-to-have
    "optional": 1      # extra
}

# Example mapping
SKILL_CATEGORIES = {
    "autocad": "core",
    "rcc": "core",
    "estimation": "core",
    "project management": "supporting",
    "quality control": "supporting",
    "construction": "core",
    "is codes": "supporting"
}

def calculate_weighted_score(matched_skills, missing_skills):
    boost = sum(SKILL_WEIGHTS[SKILL_CATEGORIES.get(s, "optional")] for s in matched_skills)
    penalty = sum(SKILL_WEIGHTS[SKILL_CATEGORIES.get(s, "optional")] for s in missing_skills)

    penalty = min(penalty, 20)  # ✅ cap penalty

    return boost, penalty

