from skill_engine import extract_skills
from domain_engine import detect_domain
from math import ceil

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
    jd_text_lower = jd_text.lower()

    jd_skills = extract_skills(jd_text_lower)
    jd_domain = detect_domain(jd_text_lower)

    feedback = []
    suggestions = []

    total_score = 0

    # ==========================
    # 1️⃣ CRITICAL SKILLS SCORE (50)
    # ==========================
    critical_skills = CRITICAL_SKILLS_BY_DOMAIN.get(jd_domain, [])
    matched_critical = [s for s in critical_skills if s in jd_skills]
    missing_critical = [s for s in critical_skills if s not in jd_skills]

    if critical_skills:
        critical_score = (len(matched_critical) / len(critical_skills)) * 50
        critical_score = ceil(critical_score)
    else:
        critical_score = 0

    total_score += critical_score

    if missing_critical:
        feedback.append(
            f"⚠️ Missing critical skills for {jd_domain}: {', '.join(missing_critical)}"
        )
        suggestions.append(
            f"Add domain-specific skills: {', '.join(missing_critical)}"
        )
    else:
        feedback.append(f"✅ Strong coverage of critical skills for {jd_domain}")

    # ==========================
    # 2️⃣ DOMAIN CLARITY SCORE (20)
    # ==========================
    if jd_domain != "Unknown":
        total_score += 20
        feedback.append(f"📌 Detected JD Domain: {jd_domain}")
    else:
        suggestions.append("Add clear role-specific keywords to define domain")

    # ==========================
    # 3️⃣ GENERIC WORDING PENALTY (15)
    # ==========================
    generic_hits = [kw for kw in GENERIC_KEYWORDS if kw in jd_text_lower]

    if not generic_hits:
        total_score += 15
        feedback.append("✅ JD language is specific and professional")
    elif len(generic_hits) <= 2:
        total_score += 7
        feedback.append(
            f"⚠️ Some generic phrases detected: {', '.join(generic_hits)}"
        )
        suggestions.append(
            "Replace generic phrases with measurable responsibilities"
        )
    else:
        feedback.append(
            f"❌ Too many generic phrases: {', '.join(generic_hits)}"
        )
        suggestions.append(
            "Rewrite JD using role-specific tools, metrics, and outcomes"
        )

    # ==========================
    # 4️⃣ SKILL DENSITY SCORE (15)
    # ==========================
    skill_count = len(jd_skills)

    if skill_count >= 10:
        total_score += 15
    elif skill_count >= 5:
        total_score += 10
    elif skill_count >= 1:
        total_score += 5

    # ==========================
    # FINAL NORMALIZED SCORE
    # ==========================
    total_score = min(total_score, 100)

    return {
        "jd_quality_score": total_score,
        "jd_domain": jd_domain,
        "matched_critical_skills": matched_critical,
        "missing_critical_skills": missing_critical,
        "jd_skills": jd_skills,
        "feedback": feedback,
        "suggestions": suggestions
    }