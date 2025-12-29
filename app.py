import streamlit as st
import os
import pandas as pd
from analytics_engine import generate_ats_analytics
import matplotlib.pyplot as plt
from jd_quality_engine import analyze_jd_quality
from ranking_engine import rank_resumes
from explanation_engine import generate_explanation
from verdict_engine import recruiter_verdict
from summary_engine import generate_summary

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("📄 AI Resume Screener (ATS)")
st.write("Upload resumes and paste Job Description to rank candidates intelligently.")

# ==========================
# SIDEBAR – ATS WEIGHTS
# ==========================
st.sidebar.subheader("⚙️ ATS Weight Controls")

skill_weight = st.sidebar.slider("Skill Importance", 0.0, 2.0, 1.0, 0.1)
experience_weight = st.sidebar.slider("Experience Importance", 0.0, 2.0, 1.0, 0.1)
cert_weight = st.sidebar.slider("Certification Importance", 0.0, 2.0, 1.0, 0.1)
domain_penalty_weight = st.sidebar.slider("Domain Penalty Severity", 0.0, 2.0, 1.0, 0.1)

weights = {
    "skill_weight": skill_weight,
    "experience_weight": experience_weight,
    "cert_weight": cert_weight,
    "domain_penalty_weight": domain_penalty_weight
}

st.sidebar.markdown("---")

# ==========================
# SIDEBAR FILTERS
# ==========================
st.sidebar.subheader("📋 Filters")

filter_domain_match = st.sidebar.checkbox("Only show domain-matched resumes")
min_score = st.sidebar.slider("Minimum Final Score (%)", 0, 100, 0)

# Placeholder (updated after ranking)
filter_skill = st.sidebar.selectbox("Filter by skill", ["None"], key="skill_filter")

sort_option = st.sidebar.selectbox(
    "Sort resumes by:",
    [
        "Final Score (High → Low)",
        "Final Score (Low → High)",
        "Matched Skills (High → Low)",
        "Confidence Level"
    ]
)

# ==========================
# UPLOAD INPUTS
# ==========================
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

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


# ==========================
# RANK BUTTON
# ==========================
if st.button("🔍 Rank Resumes"):

    if not uploaded_files or not jd_text.strip():
        st.error("❌ Upload resumes and paste Job Description.")
        st.stop()

    resume_folder = "data/test_resumes"
    os.makedirs(resume_folder, exist_ok=True)

    # Clear old test resumes
    for f in os.listdir(resume_folder):
        try:
            os.remove(os.path.join(resume_folder, f))
        except:
            pass

    for file in uploaded_files:
        with open(os.path.join(resume_folder, file.name), "wb") as f:
            f.write(file.getbuffer())

    # ==========================
    # RUN ATS ENGINE (WITH WEIGHTS ✅)
    # ==========================
    ranked_results = rank_resumes(
        resume_folder=resume_folder,
        jd_text=jd_text,
        mode="test",
        weights=weights
    )

    if not ranked_results:
        st.warning("No resumes processed.")
        st.stop()

    # ==========================
    # SUMMARY
    # ==========================
    summary = generate_summary(ranked_results)
    analytics = generate_ats_analytics(ranked_results)

    st.subheader("📊 ATS Summary Report")
    st.write(f"**Total Resumes:** {summary['total_resumes']}")
    st.write(f"**Average Score:** {summary['average_score']} %")
    st.write(f"**Best Candidate:** {summary['best_candidate']}")
    st.write(f"**Consider Count:** {summary['consider_count']}")
    st.write(f"**Reject Count:** {summary['reject_count']}")
    st.markdown("---")

    st.subheader("📈 ATS Score Distribution")

scores = analytics.get("score_distribution", [])

if scores:
    fig, ax = plt.subplots()
    ax.hist(scores, bins=10)
    ax.set_xlabel("Final ATS Score")
    ax.set_ylabel("Number of Candidates")
    ax.set_title("ATS Score Distribution")

    st.pyplot(fig)
else:
    st.info("No score data available.")

    # ==========================
    # UPDATE SKILL FILTER
    # ==========================
    all_skills = sorted({s for r in ranked_results for s in r["matched_skills"]})
    filter_skill = st.sidebar.selectbox(
        "Filter by skill",
        ["None"] + all_skills,
        key="skill_filter_updated"
    )

    # ==========================
    # APPLY FILTERS
    # ==========================
    filtered_results = ranked_results

    if filter_domain_match:
        filtered_results = [r for r in filtered_results if r["resume_domain"] == r["jd_domain"]]

    if filter_skill != "None":
        filtered_results = [r for r in filtered_results if filter_skill in r["matched_skills"]]

    filtered_results = [r for r in filtered_results if r["final_score"] >= min_score]

    # ==========================
    # SORT
    # ==========================
    if sort_option == "Final Score (High → Low)":
        filtered_results.sort(key=lambda x: x["final_score"], reverse=True)
    elif sort_option == "Final Score (Low → High)":
        filtered_results.sort(key=lambda x: x["final_score"])
    elif sort_option == "Matched Skills (High → Low)":
        filtered_results.sort(key=lambda x: len(x["matched_skills"]), reverse=True)
    else:
        conf_map = {"Low Match": 0, "Medium Match": 1, "High Match": 2}
        filtered_results.sort(key=lambda x: conf_map.get(x["confidence"], 0), reverse=True)

    # ==========================
    # DISPLAY RESULTS
    # ==========================
    st.subheader(f"🏆 Ranked Resumes ({len(filtered_results)} shown)")

    for idx, res in enumerate(filtered_results, 1):
        st.markdown(f"### {idx}. {res['resume']}")
        st.write(f"**Final Score:** {res['final_score']} %")
        st.write(f"Resume Domain: {res['resume_domain']} | JD Domain: {res['jd_domain']}")
        st.write(f"Experience: {res['experience_years']} years")
        st.write(f"Certifications: {', '.join(res['certifications']) or 'None'}")

        if res["resume_domain"] != res["jd_domain"]:
            st.warning("⚠️ Domain mismatch detected")

        st.markdown(generate_explanation(
            res["resume"],
            res["matched_skills"],
            res["missing_skills"],
            res["final_score"]
        ))
        st.write(f"**Confidence Level:** {res['confidence']}")
       # ==========================
       # 🧠 Hiring Recommendation
       # ==========================
        rec = res.get("recommendation", "Undecided")
        action = res.get("recommended_action", "")
        reasoning = res.get("recommendation_reasoning", [])

        # Color mapping
        rec_colors = {
    "Strong Hire": "#28a745",
    "Hire": "#2ecc71",
    "Hold": "#f39c12",
    "Reject": "#e74c3c"
}

    rec_color = rec_colors.get(rec, "#6c757d")

    st.markdown(
    f"""
    <div style="
        background-color:{rec_color};
        padding:12px;
        border-radius:8px;
        color:white;
        font-weight:bold;
        font-size:16px;
        margin-top:10px;
    ">
        🧠 Recommendation: {rec}  
        <br>📌 Action: {action}
    </div>
    """,
       unsafe_allow_html=True
      )
if reasoning:
    st.markdown("**📝 Recommendation Reasoning:**")
    for r in reasoning:
        st.markdown(f"- {r}")

    st.write(f"**Recruiter Verdict:** {recruiter_verdict(res['final_score'])}")
    st.markdown("---")

    # ==========================
    # EXPORT CSV
    # ==========================
    df = pd.DataFrame(ranked_results)
    report_name = "ats_report_test.csv"
    df.to_csv(report_name, index=False)

    st.download_button(
        "⬇️ Download ATS Report CSV",
        data=open(report_name, "rb"),
        file_name=report_name,
        mime="text/csv"
    )
