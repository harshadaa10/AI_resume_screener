# ===============================
# SKILL WEIGHTS BY CATEGORY
# Used by jd_skill_engine & scoring logic
# ===============================

SKILL_WEIGHTS = {

    # ===============================
    # CORE DOMAIN SKILLS (Highest Impact)
    # ===============================
    "core_hr": 5,
    "core_it": 5,
    "core_engineering": 5,
    "core_accounting": 5,
    "core_legal": 5,
    "core_finance": 5,
    "core_sales": 5,
    "core_agriculture": 5,
    "core_construction": 5,
    "core_design": 5,
    "core_marketing": 5,
    "core_management": 5,

    # ===============================
    # TOOLS & TECHNOLOGY
    # ===============================
    "software_tools": 4,
    "analytics_tools": 4,
    "ai_tools": 4,
    "crm_tools": 4,

    # ===============================
    # PROCESS / OPERATIONS
    # ===============================
    "operations": 4,
    "process_management": 3,
    "quality_control": 3,
    "compliance": 3,

    # ===============================
    # MANAGEMENT & LEADERSHIP
    # ===============================
    "management": 3,
    "leadership": 3,
    "stakeholder_management": 3,

    # ===============================
    # REGULATIONS / STANDARDS
    # ===============================
    "codes": 2,
    "laws": 2,
    "safety": 2,

    # ===============================
    # SOFT SKILLS (Lowest Impact)
    # ===============================
    "communication": 1,
    "teamwork": 1,
    "problem_solving": 1
}

# ===============================
# MUST-HAVE SKILLS (Baseline Only)
# Missing these triggers penalty,
# but NOT instant rejection
# ===============================

MUST_HAVE_SKILLS = {

    # ===============================
    # HUMAN RESOURCES
    # ===============================
    "hr": [
        "recruitment",
        "employee relations"
    ],

    # ===============================
    # INFORMATION TECHNOLOGY
    # ===============================
    "information-technology": [
        "programming",
        "database"
    ],

    # ===============================
    # ENGINEERING (Generic)
    # ===============================
    "engineering": [
        "engineering fundamentals"
    ],

    # ===============================
    # CIVIL / CONSTRUCTION
    # ===============================
    "civil": [
        "civil engineering",
        "construction"
    ],

    # ===============================
    # MECHANICAL
    # ===============================
    "mechanical": [
        "mechanical engineering",
        "manufacturing"
    ],

    # ===============================
    # ELECTRICAL
    # ===============================
    "electrical": [
        "electrical engineering",
        "power systems"
    ],

    # ===============================
    # AGRICULTURE
    # ===============================
    "agriculture": [
        "agriculture",
        "crop management"
    ],

    # ===============================
    # ACCOUNTING
    # ===============================
    "accountant": [
        "accounting",
        "taxation"
    ],

    # ===============================
    # FINANCE
    # ===============================
    "finance": [
        "financial analysis"
    ],

    # ===============================
    # BANKING
    # ===============================
    "banking": [
        "banking operations"
    ],

    # ===============================
    # LEGAL / ADVOCATE
    # ===============================
    "advocate": [
        "law",
        "legal drafting"
    ],

    # ===============================
    # SALES
    # ===============================
    "sales": [
        "sales",
        "customer handling"
    ]
}
