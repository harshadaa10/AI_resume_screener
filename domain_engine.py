from sentence_transformers import SentenceTransformer, util

# =========================================================
# LOAD MODEL ONCE
# =========================================================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================================
# DOMAIN KEYWORDS (HARD SIGNAL)
# Canonical domain names used everywhere
# =========================================================
DOMAIN_KEYWORDS = {

    "Accountant": [
        "accountant", "accounting", "tally", "gst", "taxation",
        "audit", "balance sheet", "ledger", "bookkeeping",
        "financial statements", "cost accounting"
    ],

    "Advocate": [
        "advocate", "lawyer", "legal", "litigation", "court",
        "criminal law", "civil law", "contract law",
        "legal drafting", "legal compliance"
    ],

    "Agriculture": [
        "agriculture", "farming", "crop", "agronomy",
        "soil", "irrigation", "harvest",
        "pest control", "fertilizers"
    ],

    "Apparel": [
        "apparel", "garment", "fashion industry",
        "textile", "merchandising",
        "production planning", "quality inspection"
    ],

    "Arts": [
        "art", "arts", "fine arts", "painting",
        "sculpture", "visual arts", "creative design"
    ],

    "Aviation": [
        "aviation", "aircraft", "airport", "pilot",
        "flight operations", "airline",
        "air safety", "airport management"
    ],

    "BPO": [
        "bpo", "call center", "customer support",
        "voice process", "non voice process",
        "crm", "customer handling"
    ],

    "Banking": [
        "banking", "bank", "loan", "credit", "debit",
        "relationship manager", "retail banking",
        "credit analysis"
    ],

    "Chef": [
        "chef", "cook", "culinary", "food",
        "beverages", "kitchen", "restaurant",
        "menu planning", "food safety"
    ],

    "Construction": [
        "construction", "building", "site execution",
        "contractor", "infrastructure",
        "billing", "estimation", "quality control", "safety"
    ],

    "Consultant": [
        "consultant", "consulting", "advisory",
        "strategy consulting", "management consulting",
        "business strategy"
    ],

    "Designer": [
        "designer", "design", "graphic design",
        "ui design", "ux design", "product design",
        "figma", "adobe photoshop", "illustrator"
    ],

    "Digital-Media": [
        "digital media", "digital marketing",
        "seo", "social media", "content marketing",
        "google ads", "analytics"
    ],

    "Engineering": [
        "engineer", "engineering",
        "civil engineer", "mechanical engineer",
        "electrical engineer",
        "technical design", "problem solving"
    ],

    "Finance": [
        "finance", "financial analyst",
        "investment", "portfolio",
        "wealth management", "risk analysis",
        "budgeting", "forecasting"
    ],

    "Fitness": [
        "fitness", "health", "gym",
        "trainer", "nutrition", "wellness",
        "personal trainer"
    ],

    "HR": [
        "human resources", "hr", "recruitment",
        "talent acquisition", "payroll",
        "employee relations", "hr policies",
        "performance management", "onboarding"
    ],

    "Information-Technology": [
        "it", "information technology", "software",
        "developer", "programmer", "coding",
        "data science", "machine learning",
        "database", "sql", "etl",
        "java", "python", "react",
        "web development", "testing",
        "blockchain", "security engineer",
        "network", "cloud computing", "aws", "azure"
    ],

    "Sales": [
        "sales", "business development",
        "inside sales", "field sales",
        "lead generation", "crm",
        "negotiation"
    ],

    "Architect": [
        "architect", "architecture",
        "building design", "planning",
        "autocad", "revit", "3d modeling"
    ],

    "Business-Analyst": [
        "business analyst", "ba",
        "requirement gathering",
        "process analysis",
        "documentation", "stakeholder management"
    ],

    "Education": [
        "teacher", "education",
        "lecturer", "professor",
        "faculty", "trainer",
        "curriculum development"
    ],

    "Management": [
        "management", "operations manager",
        "project manager", "program manager",
        "pmo", "leadership", "decision making"
    ],

    "Public-Relations": [
        "public relation", "pr",
        "media handling", "press release",
        "corporate communication", "brand communication"
    ]
}

# =========================================================
# DOMAIN DESCRIPTIONS (SOFT SIGNAL – EMBEDDINGS)
# =========================================================
DOMAIN_TEXTS = {
    domain: " ".join(keywords)
    for domain, keywords in DOMAIN_KEYWORDS.items()
}

DOMAIN_EMBEDDINGS = {
    domain: model.encode(text)
    for domain, text in DOMAIN_TEXTS.items()
}

# =========================================================
# DOMAIN DETECTION FUNCTION
# =========================================================
def detect_domain(text: str) -> str:
    if not text or not text.strip():
        return "Unknown"

    text_lower = text.lower()

    # ---------- 1️⃣ KEYWORD SCORING ----------
    keyword_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                score += 1
        keyword_scores[domain] = score

    best_domain = max(keyword_scores, key=keyword_scores.get)

    # Strong keyword confidence
    if keyword_scores[best_domain] >= 2:
        return best_domain

    # ---------- 2️⃣ EMBEDDING FALLBACK ----------
    text_embedding = model.encode(text)
    similarity_scores = {
        domain: util.cos_sim(text_embedding, emb).item()
        for domain, emb in DOMAIN_EMBEDDINGS.items()
    }

    return max(similarity_scores, key=similarity_scores.get)
