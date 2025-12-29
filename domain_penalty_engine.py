# domain_penalty_engine.py

RELATED_DOMAINS = {
    "HR": ["Management", "Consultant"],
    "Information-Technology": [
        "Data-Science", "Developer", "Testing", "Database",
        "ETL", "Blockchain", "Security-Engineer"
    ],
    "Construction": ["Engineering", "Architect"],
    "Finance": ["Banking", "Accountant"],
    "Designer": ["Digital-Media", "Web-Designing"],
    "Sales": ["Business-Development", "Consultant"],
    "Engineering": ["Construction", "Manufacturing"],
    "Education": ["Training", "HR"]
}

def calculate_domain_penalty(jd_domain, resume_domain):
    if jd_domain == resume_domain:
        return 0, "Perfect domain match"

    related = RELATED_DOMAINS.get(jd_domain, [])
    if resume_domain in related:
        return -5, "Related domain match"

    return -20, "Domain mismatch"
