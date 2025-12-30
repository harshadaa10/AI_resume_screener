import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

from fairness_engine import analyze_fairness
from analytics_engine import generate_ats_analytics
from ranking_engine import rank_resumes
from explanation_engine import generate_explanation
from verdict_engine import recruiter_verdict
from summary_engine import generate_summary
from human_loop_engine import save_feedback, analyze_feedback_trends

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("📄 AI Resume Screener (ATS)")
st.caption("AI-powered resume ranking with fairness, transparency & human-in-the-loop control")

# ==========================
# SESSION STATE INIT
# ==========================
if "ranked_results" not in st.session_state:
    st.session_state.ranked_results = []

# ==========================
# SIDEBAR – ATS WEIGHTS
# ==========================
st.sidebar.subheader("⚙️ ATS Weight Controls")

weights = {
    "skill": st.sidebar.slider("Skill Importance", 0.0, 2.0, 1.0, 0.1),
    "experience": st.sidebar.slider("Experience Importance", 0.0, 2.0, 1.0, 0.1),
    "cert": st.sidebar.slider("Certification Importance", 0.0, 2.0, 1.0, 0.1),
    "domain_penalty": st.sidebar.slider("Domain Penalty Severity", 0.0, 2.0, 1.0, 0.1),
}

st.sidebar.markdown("---")

# ==========================
# INPUTS
# ==========================
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True,
)

jd_text = st.text_area("Paste Job Description", height=160)

# ==========================
# RUN BUTTON
# ==========================
run = st.button("🔍 Rank Resumes")

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
st.sidebar.subheader("📋 Filters")

filter_domain_match = st.sidebar.checkbox("Only domain-matched resumes")
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

st.subheader("⚖️ Bias & Fairness Analysis")
st.metric("Acceptance Rate (%)", fairness["acceptance_rate"])
st.info(fairness["fairness_flag"])

col1, col2 = st.columns(2)
with col1:
    st.markdown("Avg Score by Domain")
    domain_df = pd.DataFrame(
        fairness["domain_avg_scores"].items(),
        columns=["Domain", "Average Score (%)"]
    )
    st.table(domain_df)

with col2:
    st.markdown("Avg Score by Experience")
    exp_df = pd.DataFrame(
        fairness["experience_avg_scores"].items(),
        columns=["Experience Level", "Average Score (%)"]
    )
    st.table(exp_df)

# ==========================
# SUMMARY & ANALYTICS
# ==========================
summary = generate_summary(filtered_results)
analytics = generate_ats_analytics(filtered_results)

st.subheader("📊 ATS Summary")
st.metric("Total Resumes", summary["total_resumes"])
st.metric("Average Score", f"{summary['average_score']:.2f} %")
st.metric("Best Candidate", summary["best_candidate"])
st.metric("Consider Count", summary["consider_count"])
st.metric("Reject Count", summary["reject_count"])

# ==========================
# SCORE DISTRIBUTION
# ==========================
st.subheader("📈 ATS Score Distribution")
scores = analytics.get("score_distribution", [])

if scores:
    fig, ax = plt.subplots()
    ax.hist(scores, bins=10)
    ax.set_xlabel("Final ATS Score")
    ax.set_ylabel("Candidates")
    st.pyplot(fig)
else:
    st.info("No score data to display.")

# ==========================
# DISPLAY RESULTS
# ==========================
st.subheader(f"🏆 Ranked Resumes ({len(filtered_results)})")

for idx, res in enumerate(filtered_results, 1):
    st.markdown(f"### {idx}. {res['resume']}")
    st.write(f"**Final Score:** {res['final_score']:.2f} %")
    st.write(f"Experience: {res['experience_years']} years")
    st.write(f"Domains: {res['resume_domain']} → {res['jd_domain']}")
    st.write(f"Confidence: {res['confidence']}")

    st.markdown(generate_explanation(
        res["resume"],
        res["matched_skills"],
        res["missing_skills"],
        res["final_score"],
    ))

    st.markdown("#### ✍️ Recruiter Override")

    human_score = st.slider(
        "Adjust Score",
        0, 100,
        int(res["final_score"]),
        key=f"s_{idx}",
    )

    human_rec = st.selectbox(
        "Override Recommendation",
        ["Strong Hire", "Hire", "Hold", "Reject"],
        key=f"r_{idx}",
    )

    notes = st.text_area("Recruiter Notes", key=f"n_{idx}")

    if st.button("💾 Save Feedback", key=f"b_{idx}"):
        save_feedback(
            res["resume"],
            res["final_score"],
            recruiter_verdict(res["final_score"]),
            human_score,
            human_rec,
            notes,
        )
        st.success("Feedback saved ✔️")

    st.markdown("---")

# ==========================
# FEEDBACK ANALYTICS
# ==========================
st.subheader("🔁 Human Feedback Learning")
stats = analyze_feedback_trends()

if stats:
    st.write(f"Total Overrides: {stats['total_overrides']}")
    st.write(f"Avg Score Adjustment: {stats['avg_score_adjustment']}")

# ==========================
# EXPORT CSV
# ==========================
df = pd.DataFrame(filtered_results)
df.to_csv("ats_report_test.csv", index=False)

st.download_button(
    "⬇️ Download ATS Report CSV",
    data=open("ats_report_test.csv", "rb"),
    file_name="ats_report_test.csv",
    mime="text/csv",
)
