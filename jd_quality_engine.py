from skill_engine import extract_skills
from domain_engine import detect_domain

# ==========================
# DOMAIN RELATIONSHIP MAP
# ==========================
RELATED_DOMAINS = {
    "HR": ["Management", "Consultant", "Education", "Public-Relations"],

    "Information-Technology": [
        "Engineering", "Business-Analyst", "Digital-Media", "Designer"
    ],

    "Engineering": ["Construction", "Architect", "Information-Technology"],

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

# ==========================
# CRITICAL SKILLS BY DOMAIN
# ==========================
CRITICAL_SKILLS_BY_DOMAIN = {

    "HR": [
        "recruitment", "employee relations", "compliance",
        "performance management", "labor law", "benefits administration"
    ],

    "Management": [
        "leadership", "team management", "strategic planning",
        "decision making", "operations"
    ],

    "Consultant": [
        "problem solving", "client management",
        "analysis", "presentation", "stakeholder management"
    ],

    "Information-Technology": [
        "python", "java", "sql", "javascript",
        "api", "cloud", "docker"
    ],

    "Engineering": [
        "design", "analysis", "autocad",
        "problem solving", "technical documentation"
    ],

    "Construction": [
        "autocad", "site management", "rcc",
        "project management", "surveying"
    ],

    "Architect": [
        "autocad", "design planning",
        "building codes", "3d modeling"
    ],

    "Finance": [
        "accounting", "financial analysis",
        "budgeting", "forecasting", "auditing"
    ],

    "Accountant": [
        "accounting", "taxation",
        "auditing", "financial reporting"
    ],

    "Banking": [
        "banking operations", "loans",
        "risk management", "compliance"
    ],

    "Sales": [
        "sales strategy", "lead generation",
        "negotiation", "crm"
    ],

    "Marketing": [
        "digital marketing", "seo",
        "branding", "campaign management"
    ],

    "Designer": [
        "photoshop", "illustrator",
        "figma", "ui/ux"
    ],

    "Digital-Media": [
        "content creation", "social media",
        "video editing", "branding"
    ],

    "Business-Analyst": [
        "requirements gathering", "process modeling",
        "data analysis", "documentation"
    ],

    "Education": [
        "teaching", "curriculum development",
        "assessment", "student management"
    ],

    "Public-Relations": [
        "media relations", "communication",
        "brand image", "event management"
    ],

    "BPO": [
        "customer handling", "communication",
        "process adherence"
    ],

    "Aviation": [
        "safety compliance", "operations",
        "engineering knowledge"
    ],

    "Apparel": [
        "textile knowledge", "design",
        "production management"
    ]
}

# ==========================
# GENERIC JD FLAGS
# ==========================
GENERIC_KEYWORDS = [
    "team player",
    "self motivated",
    "hard working",
    "excellent communication",
    "good problem solver"
]


def analyze_jd_quality(jd_text):
    """
    Analyze Job Description quality and return feedback & suggestions
    """
    jd_text_lower = jd_text.lower()
    jd_skills = extract_skills(jd_text_lower)
    jd_domain = detect_domain(jd_text_lower)

    feedback = []
    suggestions = []

    # 1️⃣ Critical skill validation
    critical_skills = CRITICAL_SKILLS_BY_DOMAIN.get(jd_domain, [])
    missing = [s for s in critical_skills if s not in jd_skills]

    if critical_skills:
        if missing:
            feedback.append(
                f"⚠️ Missing critical skills for {jd_domain}: {', '.join(missing)}"
            )
            suggestions.append(
                f"Add these domain-specific skills: {', '.join(missing)}"
            )
        else:
            feedback.append(f"✅ JD covers all critical skills for {jd_domain}")

    # 2️⃣ Generic wording detection
    generic_hits = [kw for kw in GENERIC_KEYWORDS if kw in jd_text_lower]
    if generic_hits:
        feedback.append(
            "⚠️ JD contains generic phrases: " + ", ".join(generic_hits)
        )
        suggestions.append(
            "Replace generic phrases with measurable responsibilities"
        )
    else:
        feedback.append("✅ JD language is specific and professional")

    # 3️⃣ Domain clarity
    if jd_domain == "Unknown":
        feedback.append("❌ JD domain unclear")
        suggestions.append("Add role-specific tools, technologies, or certifications")
    else:
        feedback.append(f"📌 Detected JD Domain: {jd_domain}")

    return {
        "feedback": feedback,
        "suggestions": suggestions,
        "jd_domain": jd_domain,
        "jd_skills": jd_skills
    }
