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
        "onboarding",
        "offboarding",
        "training and development",
        "succession planning",
        "compensation management",

        # HR Analytics / Modern HR
        "people analytics",
        "hr metrics",
        "workforce planning",
        "workforce insights",
        "data driven decision making",
        "attrition analysis",
        "employee engagement analytics",
        "ai tools in hr"
    ],

    # ===============================
    # INFORMATION TECHNOLOGY
    # ===============================
    "information-technology": [
        "software development",
        "programming",
        "python",
        "java",
        "javascript",
        "react",
        "node",
        "sql",
        "mongodb",
        "database",
        "etl",
        "cloud computing",
        "aws",
        "azure",
        "docker",
        "kubernetes",
        "linux",
        "machine learning",
        "deep learning",
        "data science",
        "api development",
        "web development",
        "software testing",
        "cyber security",
        "networking",
        "blockchain"
    ],

    # ===============================
    # ENGINEERING (GENERIC)
    # ===============================
    "engineering": [
        "engineering fundamentals",
        "technical analysis",
        "problem solving",
        "technical documentation",
        "quality assurance"
    ],

    # ===============================
    # CONSTRUCTION / INFRASTRUCTURE
    # ===============================
    "construction": [
        "construction",
        "site execution",
        "contractor management",
        "infrastructure projects",
        "billing",
        "estimation",
        "quality control",
        "site safety"
    ],

    # ===============================
    # CIVIL ENGINEERING
    # ===============================
    "civil": [
        "civil engineering",
        "site engineer",
        "structural engineering",
        "geotechnical engineering",
        "surveying",
        "quantity surveying",
        "rcc",
        "steel structures",
        "concrete technology",
        "foundation engineering",
        "brickwork",
        "autocad",
        "staad",
        "etabs",
        "revit",
        "ms project",
        "primavera",
        "is codes"
    ],

    # ===============================
    # ACCOUNTING / FINANCE
    # ===============================
    "accountant": [
        "accounting",
        "tally",
        "gst",
        "taxation",
        "audit",
        "balance sheet",
        "ledger",
        "bookkeeping",
        "financial reporting",
        "income tax",
        "cost accounting"
    ],

    "finance": [
        "financial analysis",
        "investment analysis",
        "portfolio management",
        "wealth management",
        "risk analysis",
        "budgeting",
        "financial forecasting"
    ],

    "banking": [
        "banking operations",
        "loan processing",
        "credit analysis",
        "debit operations",
        "relationship management",
        "retail banking"
    ],

    # ===============================
    # LEGAL / ADVOCACY
    # ===============================
    "advocate": [
        "legal drafting",
        "litigation",
        "court procedures",
        "criminal law",
        "civil law",
        "contract law",
        "legal compliance",
        "case analysis"
    ],

    # ===============================
    # AGRICULTURE
    # ===============================
    "agriculture": [
        "agriculture",
        "farming",
        "crop management",
        "agronomy",
        "soil science",
        "irrigation management",
        "harvesting",
        "fertilizers",
        "pest control"
    ],

    # ===============================
    # APPAREL / TEXTILE
    # ===============================
    "apparel": [
        "garment manufacturing",
        "textile industry",
        "fashion merchandising",
        "production planning",
        "quality inspection"
    ],

    # ===============================
    # ARTS
    # ===============================
    "arts": [
        "fine arts",
        "painting",
        "sculpture",
        "visual arts",
        "creative design"
    ],

    # ===============================
    # AVIATION
    # ===============================
    "aviation": [
        "aircraft operations",
        "airport management",
        "flight operations",
        "airline procedures",
        "aviation safety regulations"
    ],

    # ===============================
    # BPO / CUSTOMER SUPPORT
    # ===============================
    "bpo": [
        "customer support",
        "voice process",
        "non voice process",
        "crm tools",
        "customer handling",
        "escalation management",
        "service quality"
    ],

    # ===============================
    # CHEF / HOSPITALITY
    # ===============================
    "chef": [
        "culinary arts",
        "food preparation",
        "menu planning",
        "kitchen management",
        "food safety",
        "restaurant operations"
    ],

    # ===============================
    # CONSULTING
    # ===============================
    "consultant": [
        "consulting",
        "advisory services",
        "strategy consulting",
        "management consulting",
        "business strategy",
        "process improvement"
    ],

    # ===============================
    # DESIGN
    # ===============================
    "designer": [
        "graphic design",
        "ui design",
        "ux design",
        "product design",
        "adobe photoshop",
        "illustrator",
        "figma"
    ],

    # ===============================
    # DIGITAL MEDIA / MARKETING
    # ===============================
    "digital-media": [
        "digital marketing",
        "seo",
        "social media marketing",
        "content marketing",
        "google ads",
        "marketing analytics"
    ],

    # ===============================
    # FITNESS / HEALTH
    # ===============================
    "fitness": [
        "fitness training",
        "personal training",
        "nutrition",
        "wellness coaching",
        "health assessment"
    ],

    # ===============================
    # SALES
    # ===============================
    "sales": [
        "sales",
        "business development",
        "inside sales",
        "field sales",
        "lead generation",
        "crm tools",
        "negotiation skills"
    ],

    # ===============================
    # ARCHITECTURE
    # ===============================
    "architect": [
        "architecture",
        "building design",
        "planning",
        "autocad",
        "revit",
        "3d modeling"
    ],

    # ===============================
    # BUSINESS ANALYST
    # ===============================
    "business-analyst": [
        "business analysis",
        "requirement gathering",
        "process analysis",
        "documentation",
        "stakeholder management"
    ],

    # ===============================
    # EDUCATION
    # ===============================
    "education": [
        "teaching",
        "lecturing",
        "curriculum development",
        "training delivery",
        "classroom management"
    ],

    # ===============================
    # MANAGEMENT
    # ===============================
    "management": [
        "operations management",
        "project management",
        "program management",
        "pmo",
        "leadership",
        "decision making"
    ],

    # ===============================
    # PUBLIC RELATIONS
    # ===============================
    "public-relations": [
        "public relations",
        "media handling",
        "press release",
        "corporate communication",
        "brand communication"
    ]
}

# ===============================
# FLATTENED SKILL LIST
# (Used by jd_skill_engine.py)
# ===============================
SKILLS = sorted(
    {
        skill
        for domain_skills in SKILL_CONFIG.values()
        for skill in domain_skills
    }
)
