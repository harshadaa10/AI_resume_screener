from sentence_transformers import SentenceTransformer, util

# =========================================================
# LOAD MODEL ONCE
# =========================================================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================================
# DOMAIN KEYWORDS (HARD SIGNAL)
# =========================================================
DOMAIN_KEYWORDS = {

    "Accountant": [
        "accountant", "accounting", "tally", "gst", "taxation",
        "audit", "balance sheet", "ledger", "bookkeeping"
    ],

    "Advocate": [
        "advocate", "lawyer", "legal", "litigation", "court",
        "criminal law", "civil law", "contract law"
    ],

    "Agriculture": [
        "agriculture", "farming", "crop", "agronomy",
        "soil", "irrigation", "harvest"
    ],

    "Apparel": [
        "apparel", "garment", "fashion industry",
        "textile", "merchandising"
    ],

    "Arts": [
        "art", "arts", "fine arts", "painting", "sculpture"
    ],

    "Aviation": [
        "aviation", "aircraft", "airport", "pilot",
        "flight operations", "airline"
    ],

    "BPO": [
        "bpo", "call center", "customer support",
        "voice process", "non voice process"
    ],

    "Banking": [
        "banking", "bank", "loan", "credit", "debit",
        "relationship manager"
    ],

    "Chef": [
        "chef", "cook", "culinary", "food", "beverages",
        "kitchen", "restaurant"
    ],

    "Construction": [
        "construction", "building", "site execution",
        "contractor", "infrastructure"
    ],

    "Consultant": [
        "consultant", "consulting", "advisory",
        "strategy consulting", "management consulting"
    ],

    "Designer": [
        "designer", "design", "graphic design",
        "ui design", "ux design", "product design"
    ],

    "Digital-Media": [
        "digital media", "digital marketing",
        "seo", "social media", "content marketing"
    ],

    "Engineering": [
        "engineer", "engineering",
        "civil engineer", "mechanical engineer",
        "electrical engineer"
    ],

    "Finance": [
        "finance", "financial analyst",
        "investment", "portfolio", "wealth management"
    ],

    "Fitness": [
        "fitness", "health", "gym",
        "trainer", "nutrition", "wellness"
    ],

    "HR": [
        "human resources", "hr", "recruitment",
        "talent acquisition", "payroll",
        "employee relations", "hr policies"
    ],

    "Information-Technology": [
        "it", "information technology", "software",
        "developer", "programmer", "coding",
        "data science", "machine learning",
        "database", "sql", "etl",
        "java", "python", "react", "sap",
        "web development", "testing",
        "blockchain", "security engineer",
        "network", "nse network"
    ],

    "Sales": [
        "sales", "business development",
        "inside sales", "field sales",
        "lead generation", "crm"
    ],

    "Architect": [
        "architect", "architecture",
        "building design", "planning"
    ],

    "Business-Analyst": [
        "business analyst", "ba",
        "requirement gathering", "process analysis"
    ],

    "Education": [
        "teacher", "education",
        "lecturer", "professor",
        "faculty", "trainer"
    ],

    "Management": [
        "management", "operations manager",
        "project manager", "program manager",
        "pmo", "pbopmo"
    ],

    "Public-Relations": [
        "public relation", "pr",
        "media handling", "press release"
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
    text_lower = text.lower()

    # ---------- 1️⃣ KEYWORD OVERRIDE ----------
    keyword_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        keyword_scores[domain] = sum(
            1 for kw in keywords if kw in text_lower
        )

    best_domain = max(keyword_scores, key=keyword_scores.get)

    # Strong confidence threshold
    if keyword_scores[best_domain] >= 2:
        return best_domain

    # ---------- 2️⃣ EMBEDDING FALLBACK ----------
    text_embedding = model.encode(text)
    similarity_scores = {
        domain: util.cos_sim(text_embedding, emb).item()
        for domain, emb in DOMAIN_EMBEDDINGS.items()
    }

    return max(similarity_scores, key=similarity_scores.get)
