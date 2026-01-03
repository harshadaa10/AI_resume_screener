import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

from fairness_engine import analyze_fairness
from analytics_engine import generate_ats_analytics
from ranking_engine import rank_resumes
from explanation_engine import generate_explainability
from verdict_engine import recruiter_verdict
from summary_engine import generate_summary
from human_loop_engine import save_feedback, analyze_feedback_trends
from resume_fraud_engine import detect_resume_fraud
from bias_engine import analyze_bias
from jd_llm_engine import extract_skills_from_jd


# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Professional ATS Resume Screener powered by AI"},
)

# ==========================
# CUSTOM CSS STYLING
# ==========================
st.markdown(
    """
    <style>
    /* Main Color Scheme */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #06A77D;
        --danger-color: #D62839;
        --light-bg: #F8F9FA;
        --dark-bg: #1a1a1a;
    }

    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Header Styling */
    h1 {
        color: #2E86AB !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 5px !important;
    }

    h2 {
        color: #2E86AB !important;
        font-weight: 600 !important;
        border-bottom: 3px solid #F18F01 !important;
        padding-bottom: 10px !important;
    }

    h3 {
        color: #A23B72 !important;
        font-weight: 600 !important;
    }

    /* Subheader Caption */
    .subtitle {
        font-size: 1.1rem !important;
        color: #555 !important;
        margin-bottom: 20px !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E86AB 0%, #1b5a8f 100%) !important;
        padding-top: 20px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 10px !important;
    }

    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] .stSlider {
        margin: 15px 0 !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #2E86AB 0%, #1b5a8f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(46, 134, 171, 0.3) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1b5a8f 0%, #0f3554 100%) !important;
        box-shadow: 0 6px 12px rgba(46, 134, 171, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Input Styling */
    .stTextArea textarea {
        border: 2px solid #E0E0E0 !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 12px !important;
    }

    .stTextArea textarea:focus {
        border-color: #2E86AB !important;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1) !important;
    }

    .stFileUploader {
        border: 2px dashed #2E86AB !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }

    /* Metric Cards */
    .metric-card {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
        border-left: 4px solid #2E86AB !important;
    }

    [data-testid="metric-container"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
        border-top: 4px solid #F18F01 !important;
    }

    /* Info Box */
    .stInfo {
        background-color: #E3F2FD !important;
        border: 2px solid #2E86AB !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #1565C0 !important;
    }

    /* Success Box */
    .stSuccess {
        background-color: #E8F5E9 !important;
        border: 2px solid #06A77D !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #2E7D32 !important;
    }

    /* Error Box */
    .stError {
        background-color: #FFEBEE !important;
        border: 2px solid #D62839 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #C62828 !important;
    }

    /* Table Styling */
    table {
        width: 100% !important;
        border-collapse: collapse !important;
    }

    table th {
        background: linear-gradient(90deg, #2E86AB 0%, #1b5a8f 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px !important;
        text-align: left !important;
    }

    table td {
        padding: 12px !important;
        border-bottom: 1px solid #E0E0E0 !important;
    }

    table tr:hover {
        background-color: #F5F5F5 !important;
    }

    /* Divider */
    hr {
        margin: 30px 0 !important;
        border: 0 !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #2E86AB, transparent) !important;
    }

    /* Selectbox & Multiselect */
    .stSelectbox select, .stMultiSelect {
        border-radius: 8px !important;
        border: 2px solid #E0E0E0 !important;
    }

    .stSelectbox select:focus {
        border-color: #2E86AB !important;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1) !important;
    }

    /* Checkbox */
    .stCheckbox {
        margin: 10px 0 !important;
    }

    /* Slider */
    .stSlider {
        margin: 15px 0 !important;
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #06A77D 0%, #038a63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(90deg, #038a63 0%, #026d4f 100%) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f0f2f6 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Code Block */
    .stCode {
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
    }

    /* Markdown Links */
    a {
        color: #2E86AB !important;
        text-decoration: none !important;
        font-weight: 500 !important;
    }

    a:hover {
        color: #1b5a8f !important;
        text-decoration: underline !important;
    }

    /* Custom Card Style */
    .custom-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin: 10px 0;
        border-left: 4px solid #2E86AB;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================
# HEADER
# ==========================
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 📄")
with col2:
    st.markdown("# AI Resume Screener (ATS)")

st.markdown(
    '<p class="subtitle">🎯 AI-powered resume ranking with fairness, transparency & human-in-the-loop control</p>',
    unsafe_allow_html=True,
)

# ==========================
# SESSION STATE INIT
# ==========================
if "ranked_results" not in st.session_state:
    st.session_state.ranked_results = []

# ==========================
# SIDEBAR – ATS WEIGHTS
# ==========================
st.sidebar.markdown("## ⚙️ ATS Configuration")
st.sidebar.markdown("Adjust scoring weights for your hiring criteria:")

weights = {
    "skill": st.sidebar.slider("🎯 Skill Importance", 0.0, 2.0, 1.0, 0.1),
    "experience": st.sidebar.slider("💼 Experience Importance", 0.0, 2.0, 1.0, 0.1),
    "cert": st.sidebar.slider("🏆 Certification Importance", 0.0, 2.0, 1.0, 0.1),
    "domain_penalty": st.sidebar.slider("⚠️ Domain Penalty Severity", 0.0, 2.0, 1.0, 0.1),
}

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
    <p style="color: white; margin: 0;"><strong>💡 Tips:</strong><br>
    Higher weights give more importance to that factor in scoring.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# MAIN INPUTS SECTION
# ==========================
st.markdown("---")
st.markdown("## 📥 Upload & Configure")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Resume Upload")
    uploaded_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

with col2:
    st.markdown("### Job Description")
    jd_text = st.text_area(
        "Paste Job Description",
        height=150,
        label_visibility="collapsed",
        placeholder="Enter the job description here...",
    )
    if jd_text.strip():
        st.success(f"✅ {len(jd_text.split())} words entered")

# ==========================
# RUN BUTTON
# ==========================
col_btn_space, col_btn = st.columns([3, 1])
with col_btn:
    run = st.button("🔍 Rank Resumes", width="stretch")

if run:
    if not uploaded_files or not jd_text.strip():
        st.error("❌ Please upload resumes and paste a Job Description.")
        st.stop()

    resume_folder = "data/test_resumes"
    os.makedirs(resume_folder, exist_ok=True)

    for f in os.listdir(resume_folder):
        try:
            os.remove(os.path.join(resume_folder, f))
        except:
            pass

    for file in uploaded_files:
        with open(os.path.join(resume_folder, file.name), "wb") as f:
            f.write(file.getbuffer())

    st.session_state.ranked_results = rank_resumes(
        resume_folder=resume_folder,
        jd_text=jd_text,
        mode="test",
        weights=weights,
    )

# ==========================
# STOP IF NOTHING RAN
# ==========================
if not st.session_state.ranked_results:
    st.info("Upload resumes & click **Rank Resumes** to begin.")
    st.stop()

ranked_results = st.session_state.ranked_results

# ==========================
# SIDEBAR – FILTERS
# ==========================
st.sidebar.markdown("---")
st.sidebar.markdown("## 📋 Filter & Sort Results")

filter_domain_match = st.sidebar.checkbox("✓ Only domain-matched resumes")
min_score = st.sidebar.slider("Minimum Final Score (%)", 0, 100, 0)

all_skills = sorted({s for r in ranked_results for s in r["matched_skills"]})
filter_skill = st.sidebar.selectbox("Filter by Skill", ["None"] + all_skills)

confidence_filter = st.sidebar.selectbox(
    "Filter by Confidence",
    ["All", "High Match", "Medium Match", "Low Match"]
)

sort_option = st.sidebar.selectbox(
    "Sort resumes by",
    [
        "Final Score (High → Low)",
        "Final Score (Low → High)",
        "Matched Skills (High → Low)",
        "Confidence Level",
    ],
)

# ==========================
# APPLY FILTERS
# ==========================
filtered_results = ranked_results

if filter_domain_match:
    filtered_results = [
        r for r in filtered_results
        if r["resume_domain"] == r["jd_domain"]
    ]

if filter_skill != "None":
    filtered_results = [
        r for r in filtered_results
        if filter_skill in r["matched_skills"]
    ]

if confidence_filter != "All":
    filtered_results = [
        r for r in filtered_results
        if r["confidence"] == confidence_filter
    ]

filtered_results = [
    r for r in filtered_results
    if r["final_score"] >= min_score
]

# ==========================
# SORTING
# ==========================
if sort_option == "Final Score (High → Low)":
    filtered_results.sort(key=lambda x: x["final_score"], reverse=True)
elif sort_option == "Final Score (Low → High)":
    filtered_results.sort(key=lambda x: x["final_score"])
elif sort_option == "Matched Skills (High → Low)":
    filtered_results.sort(key=lambda x: len(x["matched_skills"]), reverse=True)
else:
    conf_map = {"Low Match": 0, "Medium Match": 1, "High Match": 2}
    filtered_results.sort(
        key=lambda x: conf_map.get(x["confidence"], 0),
        reverse=True,
    )

# ==========================
# FAIRNESS ANALYSIS
# ==========================
fairness = analyze_fairness(filtered_results)

st.markdown("---")
st.markdown("## ⚖️ Bias & Fairness Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    acceptance_rate = fairness["acceptance_rate"]
    st.metric("Acceptance Rate", f"{acceptance_rate:.1f}%")

with col2:
    total_resumes = len(filtered_results)
    st.metric("Total Evaluated", total_resumes)

with col3:
    avg_score = sum(r["final_score"] for r in filtered_results) / len(filtered_results) if filtered_results else 0
    st.metric("Average Score", f"{avg_score:.1f}%")

# Fairness flag with better styling
fairness_flag = fairness["fairness_flag"]
if "⚠️" in fairness_flag:
    st.warning(fairness_flag)
elif "✅" in fairness_flag:
    st.success(fairness_flag)
else:
    st.info(fairness_flag)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Avg Score by Domain")
    domain_df = pd.DataFrame(
        fairness["domain_avg_scores"].items(),
        columns=["Domain", "Average Score (%)"]
    )
    domain_df["Average Score (%)"] = domain_df["Average Score (%)"].round(2)
    st.dataframe(domain_df, width="stretch", hide_index=True)

with col2:
    st.markdown("### Avg Score by Experience")
    exp_df = pd.DataFrame(
        fairness["experience_avg_scores"].items(),
        columns=["Experience Level", "Average Score (%)"]
    )
    exp_df["Average Score (%)"] = exp_df["Average Score (%)"].round(2)
    st.dataframe(exp_df, width="stretch", hide_index=True)

# ==========================
# SUMMARY & ANALYTICS
# ==========================
st.markdown("---")
st.markdown("## 📊 ATS Summary & Insights")

summary = generate_summary(filtered_results)
analytics = generate_ats_analytics(filtered_results)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Resumes", summary["total_resumes"])

with col2:
    st.metric("Average Score", f"{summary['average_score']:.2f}%")

with col3:
    st.metric("Strong Hires", summary["consider_count"])

with col4:
    st.metric("Rejections", summary["reject_count"])



# ==========================
# SCORE DISTRIBUTION
# ==========================
st.markdown("---")
st.markdown("## 📈 Score Distribution Analysis")

scores = analytics.get("score_distribution", [])

if scores:
    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(scores, bins=15, color="#2E86AB", edgecolor="#1b5a8f", alpha=0.7)
        ax.set_xlabel("Final ATS Score (%)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Number of Candidates", fontsize=11, fontweight="bold")
        ax.set_title("Resume Score Distribution", fontsize=13, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, width="stretch")
    
    with col2:
        st.markdown("### Score Stats")
        st.metric("Highest Score", f"{max(scores):.1f}%")
        st.metric("Lowest Score", f"{min(scores):.1f}%")
        st.metric("Median Score", f"{sorted(scores)[len(scores)//2]:.1f}%")
else:
    st.info("No score data to display.")

# ==========================
# DISPLAY RESULTS
# ==========================
st.markdown("---")
st.markdown(f"## 🏆 Ranked Resumes ({len(filtered_results)})")

if not filtered_results:
    st.warning("No resumes match the current filters.")
else:
    for idx, res in enumerate(filtered_results, 1):
        # Confidence badge
        conf_color = {
            "High Match": "#06A77D",
            "Medium Match": "#F18F01",
            "Low Match": "#D62839",
        }
        conf_badge = f'<span style="background:{conf_color.get(res["confidence"], "#999")}; color:white; padding:5px 10px; border-radius:5px; font-weight:bold;">{res["confidence"]}</span>'
        
        # Score color
        score = res["final_score"]
        if score >= 75:
            score_color = "#06A77D"
            score_emoji = "⭐"
        elif score >= 50:
            score_color = "#F18F01"
            score_emoji = "👍"
        else:
            score_color = "#D62839"
            score_emoji = "📍"
        
        st.markdown(
            f"""
            <div style="background: white; border-radius: 12px; padding: 20px; margin: 15px 0; 
                    border-left: 5px solid {score_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="margin: 0; color: #2E86AB;">{idx}. {res['resume']}</h3>
                    <div>{conf_badge}</div>
                </div>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #E0E0E0;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div><strong>Final Score</strong><br><span style="font-size: 1.5rem; color: {score_color}; font-weight: bold;">{score_emoji} {score:.1f}%</span></div>
                    <div><strong>Experience</strong><br>{res['experience_years']} years</div>
                    <div><strong>Domain Match</strong><br>{res['resume_domain']} → {res['jd_domain']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
       # -----------------------------
# 🧠 Explainability Section
# -----------------------------
exp = generate_explainability(res)

st.markdown("### 🧠 Recruiter Explanation")

st.write(f"**Verdict:** {exp['verdict']}")

if exp["strengths"]:
    st.markdown("**Strengths:**")
    for s in exp["strengths"]:
        st.write("•", s)

if exp["concerns"]:
    st.markdown("**Concerns:**")
    for c in exp["concerns"]:
        st.write("•", c)


        # Recruiter Override Section
unique_id = f"{idx}_{res['resume']}"

with st.expander(f"✍️ Recruiter Notes & Override - {res['resume']}", expanded=False):
    col1, col2 = st.columns([1, 1])

    with col1:
        human_score = st.slider(
            "Adjust Score",
            0, 100,
            int(res["final_score"]),
            key=f"s_{unique_id}",
        )

    with col2:
        human_rec = st.selectbox(
            "Override Recommendation",
            ["Strong Hire", "Hire", "Hold", "Reject"],
            key=f"r_{unique_id}",
        )

    notes = st.text_area(
        "Recruiter Notes",
        key=f"n_{unique_id}",
        height=80,
    )

    col_save, col_space = st.columns([1, 4])
    with col_save:
        if st.button(
            "💾 Save Feedback",
            key=f"b_{unique_id}",
            width="stretch",
        ):
            save_feedback(
                res["resume"],
                res["final_score"],
                recruiter_verdict(res["final_score"]),
                human_score,
                human_rec,
                notes,
            )
            st.success("✅ Feedback saved!")

# ==========================
# FEEDBACK ANALYTICS
# ==========================
st.markdown("---")
st.markdown("## 🔁 Human Feedback Learning")

stats = analyze_feedback_trends()

if stats:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Overrides", stats['total_overrides'])
    with col2:
        st.metric("Avg Score Adjustment", f"{stats['avg_score_adjustment']:.1f}%")
    with col3:
        st.metric("Learning Rate", "Active")
else:
    st.info("💡 No feedback recorded yet. Start saving feedback to track hiring patterns!")

# ==========================
# EXPORT CSV
# ==========================
st.markdown("---")
st.markdown("## 💾 Export Report")

df = pd.DataFrame(filtered_results)
df.to_csv("ats_report_test.csv", index=False)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.download_button(
        "📥 Download ATS Report (CSV)",
        data=open("ats_report_test.csv", "rb"),
        file_name="ats_report_test.csv",
        mime="text/csv",
       width="stretch",
    )

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; margin-top: 30px; padding: 20px;">
        <p><strong>AI Resume Screener</strong> | Made by Harshada Suryawanshi</p>
        <p style="font-size: 0.9em;">© 2024 - Professional ATS Solution</p>
    </div>
    """,
    unsafe_allow_html=True,
)
