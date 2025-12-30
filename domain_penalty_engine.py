# =========================================================
# DOMAIN PENALTY ENGINE
# =========================================================

# Canonical related-domain mapping
# Used to reduce penalty for transferable domains
RELATED_DOMAINS = {

    "HR": [
        "Management",
        "Consultant",
        "Education",
        "Public-Relations"
    ],

    "Information-Technology": [
        "Engineering",
        "Business-Analyst",
        "Digital-Media",
        "Designer"
    ],

    "Engineering": [
        "Construction",
        "Architect",
        "Information-Technology"
    ],

    "Construction": [
        "Engineering",
        "Architect"
    ],

    "Architect": [
        "Construction",
        "Engineering",
        "Designer"
    ],

    "Finance": [
        "Banking",
        "Accountant",
        "Management"
    ],

    "Accountant": [
        "Finance",
        "Banking"
    ],

    "Banking": [
        "Finance",
        "Accountant",
        "Sales"
    ],

    "Sales": [
        "Marketing",
        "Consultant",
        "Management",
        "Public-Relations"
    ],

    "Consultant": [
        "Management",
        "Business-Analyst",
        "Sales"
    ],

    "Designer": [
        "Digital-Media",
        "Architect",
        "Information-Technology"
    ],

    "Digital-Media": [
        "Designer",
        "Sales",
        "Public-Relations"
    ],

    "Business-Analyst": [
        "Management",
        "Consultant",
        "Information-Technology"
    ],

    "Education": [
        "HR",
        "Management"
    ],

    "Public-Relations": [
        "Sales",
        "Digital-Media",
        "Management"
    ],

    "Agriculture": [
        "Management"
    ],

    "BPO": [
        "Sales",
        "HR"
    ],

    "Chef": [
        "Hospitality"
    ],

    "Fitness": [
        "Health"
    ],

    "Arts": [
        "Designer"
    ],

    "Aviation": [
        "Engineering",
        "Management"
    ],

    "Apparel": [
        "Designer",
        "Management"
    ]
}

# =========================================================
# DOMAIN PENALTY LOGIC
# =========================================================
def calculate_domain_penalty(jd_domain: str, resume_domain: str):
    """
    Returns:
        penalty (int): negative score impact
        reason (str): human-readable explanation
    """

    # ---------- SAFETY ----------
    if not jd_domain or not resume_domain:
        return -10, "Domain unclear – partial penalty applied"

    # ---------- PERFECT MATCH ----------
    if jd_domain == resume_domain:
        return 0, "Perfect domain match"

    # ---------- RELATED DOMAIN ----------
    related = RELATED_DOMAINS.get(jd_domain, [])
    if resume_domain in related:
        return -5, "Related domain – transferable skills detected"

    # ---------- WEAK TRANSFER ----------
    reverse_related = RELATED_DOMAINS.get(resume_domain, [])
    if jd_domain in reverse_related:
        return -8, "Partially related domain – limited transferability"

    # ---------- COMPLETE MISMATCH ----------
    return -20, "Domain mismatch – low relevance to job role"
