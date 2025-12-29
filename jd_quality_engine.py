from skill_engine import extract_skills
from domain_engine import detect_domain

CRITICAL_SKILLS_BY_DOMAIN = {
    "HR": ["recruitment", "employee relations", "compliance", "performance evaluations", "benefits administration", "labor law"],
    "Information-Technology": ["python", "java", "sql", "react", "aws", "devops", "docker"],
    "Finance": ["accounting", "budgeting", "forecasting", "financial analysis", "auditing"],
    "Construction": ["autocad", "project management", "structural engineering", "rcc", "surveying"],
    "Designer": ["photoshop", "illustrator", "figma", "web design", "ui/ux"],
    # add more domains & critical skills as needed
}

GENERIC_KEYWORDS = [
    "strong communication", "team player", "self motivated", "excellent skills", "good problem solver"
]


def analyze_jd_quality(jd_text):
    """
    Analyze Job Description quality and return insights along with improvement suggestions.
    """
    jd_text_lower = jd_text.lower()
    jd_skills = extract_skills(jd_text_lower)
    jd_domain = detect_domain(jd_text_lower)

    feedback = []
    suggestions = []

    # 1️⃣ Critical skills check
    critical_skills = CRITICAL_SKILLS_BY_DOMAIN.get(jd_domain, [])
    missing_critical_skills = [skill for skill in critical_skills if skill not in jd_skills]

    if missing_critical_skills:
        feedback.append(f"⚠️ JD is missing critical skills for {jd_domain}: {', '.join(missing_critical_skills)}")
        suggestions.append(f"Add these skills to JD: {', '.join(missing_critical_skills)}")
    else:
        feedback.append(f"✅ JD covers all critical skills for {jd_domain}")

    # 2️⃣ Generic JD warning
    generic_hits = [kw for kw in GENERIC_KEYWORDS if kw in jd_text_lower]
    if generic_hits:
        feedback.append("⚠️ JD contains generic phrases that may reduce candidate clarity: " +
                        ", ".join(generic_hits))
        suggestions.append("Replace generic phrases with specific skills or responsibilities")
    else:
        feedback.append("✅ JD is concise and specific")

    # 3️⃣ Domain clarity
    if jd_domain == "Unknown":
        feedback.append("❌ Unable to detect JD domain. Please make it more descriptive.")
        suggestions.append("Include domain-specific keywords in JD")
    else:
        feedback.append(f"📌 Detected JD Domain: {jd_domain}")

    return {
        "feedback": feedback,
        "suggestions": suggestions,
        "jd_domain": jd_domain,
        "jd_skills": jd_skills
    }
