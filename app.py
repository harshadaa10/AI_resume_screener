import streamlit as st
import os
import pandas as pd

from ranking_engine import rank_resumes
from confidence_engine import confidence_level
from explanation_engine import generate_explanation
from verdict_engine import recruiter_verdict
from summary_engine import generate_summary  

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="AI Resume Screener",
    layout="wide"
)

st.title("📄 AI Resume Screener (ATS)")
st.write("Upload resumes and paste Job Description to rank candidates intelligently.")

# ==========================
# SIDEBAR FILTERS & SORTING
# ==========================
st.sidebar.subheader("📋 Filters & Sorting")

filter_domain_match = st.sidebar.checkbox(
    "Only show domain-matched resumes",
    value=False
)

filter_skill = st.sidebar.selectbox(
    "Filter by skill",
    ["None"],
    key="skill_filter"
)

min_score = st.sidebar.slider(
    "Minimum Final Score (%)",
    0, 100, 0
)

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
# UPLOAD RESUMES & JD
# ==========================
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

jd_text = st.text_area(
    "Paste Job Description",
    height=200
)

# ==========================
# RANK RESUMES BUTTON
# ==========================
if st.button("🔍 Rank Resumes"):

    if not uploaded_files or not jd_text.strip():
        st.error("❌ Please upload resumes and paste a Job Description.")
        st.stop()

    st.success("Processing resumes...")

    # ==========================
    # SAVE TEST RESUMES
    # ==========================
    resume_folder = "data/test_resumes"
    os.makedirs(resume_folder, exist_ok=True)

    # Clear old test resumes
    for f in os.listdir(resume_folder):
        try:
            os.remove(os.path.join(resume_folder, f))
        except:
            pass

    # Save uploaded PDFs
    for file in uploaded_files:
        with open(os.path.join(resume_folder, file.name), "wb") as f:
            f.write(file.getbuffer())

    # ==========================
    # RUN ATS ENGINE
    # ==========================
    ranked_results = rank_resumes(
        resume_folder=resume_folder,
        jd_text=jd_text,
        mode="test"
    )

    if not ranked_results:
        st.warning("⚠️ No resumes were processed.")
        st.stop()

    # ==========================
    # ATS SUMMARY
    # ==========================
    summary = generate_summary(ranked_results)

    st.subheader("📊 ATS Summary Report")
    st.write(f"**Total Resumes Processed:** {summary['total_resumes']}")
    st.write(f"**Average ATS Score:** {summary['average_score']} %")
    st.write(f"**Best Candidate:** {summary['best_candidate']}")
    st.write(f"**Consider Count:** {summary['consider_count']}")
    st.write(f"**Reject Count:** {summary['reject_count']}")
    st.markdown("---")

    # ==========================
    # SKILL LIST FOR FILTERING
    # ==========================
    all_skills = sorted(
        list({skill for res in ranked_results for skill in res["matched_skills"]})
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

    filtered_results = [
        r for r in filtered_results
        if r["final_score"] >= min_score
    ]

    # ==========================
    # APPLY SORTING
    # ==========================
    if sort_option == "Final Score (High → Low)":
        filtered_results.sort(key=lambda x: x["final_score"], reverse=True)

    elif sort_option == "Final Score (Low → High)":
        filtered_results.sort(key=lambda x: x["final_score"])

    elif sort_option == "Matched Skills (High → Low)":
        filtered_results.sort(
            key=lambda x: len(x["matched_skills"]),
            reverse=True
        )

    elif sort_option == "Confidence Level":
        conf_map = {
            "Low Match": 0,
            "Medium Match": 1,
            "High Match": 2
        }
        filtered_results.sort(
            key=lambda x: conf_map.get(x["confidence"], 0),
            reverse=True
        )

    # ==========================
    # DISPLAY RESULTS
    # ==========================
    st.subheader(f"🏆 Ranked Resumes ({len(filtered_results)} shown)")

    for idx, res in enumerate(filtered_results, start=1):
        st.markdown(f"### {idx}. {res['resume']}")
        st.write(f"**Final Score:** {res['final_score']} %")
        st.write(f"Base Similarity: {res['base_score']} %")
        st.write(f"Skill Boost: +{res['boost']}")
        st.write(f"Penalty: -{res['penalty']}")
        st.write(f"Resume Domain: {res['resume_domain']}")
        st.write(f"JD Domain: {res['jd_domain']}")

        if res["resume_domain"] != res["jd_domain"]:
            st.warning("⚠️ Domain mismatch detected")

        # Matched skills
        if res["matched_skills"]:
            matched_html = " ".join([
                f"<span style='background:#d4edda;color:#155724;padding:4px 7px;border-radius:6px;margin-right:4px'>{s}</span>"
                for s in res["matched_skills"]
            ])
        else:
            matched_html = "None"

        st.markdown(
            f"✔ **Matched Skills:** {matched_html}",
            unsafe_allow_html=True
        )

        # Missing skills
        if res["missing_skills"]:
            missing_html = " ".join([
                f"<span style='background:#f8d7da;color:#721c24;padding:4px 7px;border-radius:6px;margin-right:4px'>{s}</span>"
                for s in res["missing_skills"]
            ])
        else:
            missing_html = "None"

        st.markdown(
            f"✖ **Missing Skills:** {missing_html}",
            unsafe_allow_html=True
        )

        st.write(f"**Confidence Level:** {res['confidence']}")

        st.markdown(
            generate_explanation(
                res["resume"],
                res["matched_skills"],
                res["missing_skills"],
                res["final_score"]
            )
        )

        st.write(
            f"**Recruiter Verdict:** {recruiter_verdict(res['final_score'])}"
        )

        st.markdown("---")

    # ==========================
    # EXPORT CSV
    # ==========================
    df = pd.DataFrame(ranked_results)
    report_name = "ats_report_test.csv"
    df.to_csv(report_name, index=False)

    st.success(f"📁 ATS Report saved as `{report_name}`")

    with open(report_name, "rb") as f:
        st.download_button(
            "⬇️ Download ATS Report CSV",
            data=f,
            file_name=report_name,
            mime="text/csv"
        )
