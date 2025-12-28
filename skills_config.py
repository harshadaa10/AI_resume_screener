# ===============================
# SKILL CONFIG BY DOMAIN
# ===============================

SKILL_CONFIG = {

    # ===============================
    # HUMAN RESOURCES
    # ===============================
    "hr": [
        "recruitment",
        "talent acquisition",
        "employee relations",
        "performance management",
        "performance appraisal",
        "payroll",
        "benefits administration",
        "labor law",
        "compliance",
        "hr policies",
        "hris",
        "people management",
        "onboarding",
        "offboarding",
        "training and development",
        "succession planning",
        "shrm",
        "phr",
        "compensation management"
    ],

    # ===============================
    # INFORMATION TECHNOLOGY
    # ===============================
    "it": [
        "python", "java", "javascript", "react",
        "node", "sql", "mongodb", "aws",
        "docker", "kubernetes", "linux",
        "machine learning", "deep learning",
        "data science", "api", "cloud computing"
    ],

    # ===============================
    # CIVIL / CONSTRUCTION
    # ===============================
    "civil": [
        "civil engineering", "construction",
        "site engineer", "structural engineering",
        "geotechnical", "surveying",
        "quantity surveying",
        "rcc", "steel structures",
        "concrete", "foundation",
        "brickwork", "autocad",
        "staad", "etabs", "revit",
        "ms project", "primavera",
        "billing", "estimation",
        "cost control", "quality control",
        "safety", "is codes"
    ],

    # ===============================
    # MANAGEMENT / BUSINESS
    # ===============================
    "management": [
        "project management",
        "operations management",
        "business analysis",
        "strategic planning",
        "stakeholder management",
        "risk management",
        "process improvement",
        "leadership",
        "team management"
    ]
}
# ===============================
# FLATTENED SKILL LIST
# (Used by skill_engine.py)
# ===============================
SKILLS = sorted(
    set(
        skill
        for domain_skills in SKILL_CONFIG.values()
        for skill in domain_skills
    )
)