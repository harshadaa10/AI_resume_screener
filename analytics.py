import streamlit as st
import pandas as pd
import plotly.express as px
from analytics_engine import generate_ats_analytics
from domain_engine import ALL_DOMAINS

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="ATS Analytics Dashboard",
    layout="wide"
)

st.title("📊 ATS Analytics Dashboard")
st.write("Advanced insights and visual analytics for resume screening.")

# ==========================
# SIDEBAR FILTERS
# ==========================
st.sidebar.subheader("📋 Filters")

filter_confidence = st.sidebar.multiselect(
    "Confidence Level",
    ["Low Match", "Medium Match", "High Match"],
    default=["Low Match", "Medium Match", "High Match"]
)

filter_skill = st.sidebar.selectbox(
    "Filter by Skill",
    ["None"],
    key="skill_filter"
)

filter_domains = st.sidebar.multiselect(
    "Resume Domains",
    ALL_DOMAINS,
    default=ALL_DOMAINS
)

min_score = st.sidebar.slider(
    "Minimum Final Score (%)",
    0, 100, 0
)

# ==========================
# UPLOAD CSV
# ==========================
uploaded_file = st.file_uploader(
    "Upload ATS Report CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    ranked_results = df.to_dict(orient="records")

    # ==========================
    # APPLY FILTERS
    # ==========================
    filtered = ranked_results

    filtered = [r for r in filtered if r["confidence"] in filter_confidence]

    if filter_skill != "None":
        filtered = [r for r in filtered if filter_skill in r["matched_skills"]]

    filtered = [r for r in filtered if r["resume_domain"] in filter_domains]
    filtered = [r for r in filtered if r["final_score"] >= min_score]

    # ==========================
    # ANALYTICS
    # ==========================
    analytics = generate_ats_analytics(filtered)

    # ==========================
    # SUMMARY METRICS
    # ==========================
    st.subheader("📌 Key Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Resumes", len(filtered))
    c2.metric("Domain Matches", analytics["domain_match"]["Matched"])
    c3.metric("Domain Mismatches", analytics["domain_match"]["Mismatched"])
    c4.metric(
        "Avg ATS Score",
        round(
            sum(analytics["score_distribution"]) / len(analytics["score_distribution"]), 2
        ) if analytics["score_distribution"] else 0
    )

    st.markdown("---")

    # ==========================
    # ROW 1 → SCORE & DOMAIN
    # ==========================
    col1, col2 = st.columns(2)

    with col1:
        df_scores = pd.DataFrame({"Score": analytics["score_distribution"]})
        fig_score = px.histogram(
            df_scores,
            x="Score",
            nbins=10,
            title="Final ATS Score Distribution",
            color_discrete_sequence=["#4CAF50"]
        )
        st.plotly_chart(fig_score, use_container_width=True)

    with col2:
        df_domain = pd.DataFrame({
            "Status": analytics["domain_match"].keys(),
            "Count": analytics["domain_match"].values()
        })
        fig_domain = px.pie(
            df_domain,
            names="Status",
            values="Count",
            title="Domain Match Analysis",
            color="Status",
            color_discrete_map={
                "Matched": "#2ECC71",
                "Mismatched": "#E74C3C"
            }
        )
        st.plotly_chart(fig_domain, use_container_width=True)

    # ==========================
    # ROW 2 → CONFIDENCE & EXPERIENCE
    # ==========================
    col3, col4 = st.columns(2)

    with col3:
        df_conf = pd.DataFrame({
            "Confidence": analytics["confidence_levels"].keys(),
            "Count": analytics["confidence_levels"].values()
        })
        fig_conf = px.bar(
            df_conf,
            x="Confidence",
            y="Count",
            color="Confidence",
            title="Confidence Level Distribution",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_conf, use_container_width=True)

    with col4:
        exp_df = pd.DataFrame(analytics["experience_vs_score"])
        fig_exp = px.scatter(
            exp_df,
            x="experience_years",
            y="final_score",
            color="final_score",
            title="Experience vs Final ATS Score",
            labels={
                "experience_years": "Experience (Years)",
                "final_score": "Final Score"
            },
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_exp, use_container_width=True)

    # ==========================
    # ROW 3 → SKILLS ANALYSIS
    # ==========================
    col5, col6 = st.columns(2)

    with col5:
        matched = analytics["matched_skills"]
        if matched:
            df_matched = pd.DataFrame(
                matched.items(), columns=["Skill", "Count"]
            ).sort_values("Count", ascending=False).head(10)

            fig_match = px.bar(
                df_matched,
                x="Count",
                y="Skill",
                orientation="h",
                title="Top Matched Skills",
                color="Count",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_match, use_container_width=True)

    with col6:
        missing = analytics["missing_skills"]
        if missing:
            df_missing = pd.DataFrame(
                missing.items(), columns=["Skill", "Count"]
            ).sort_values("Count", ascending=False).head(10)

            fig_missing = px.bar(
                df_missing,
                x="Count",
                y="Skill",
                orientation="h",
                title="Top Missing Skills",
                color="Count",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_missing, use_container_width=True)

    # ==========================
    # 🧠 ROW 4 → RECOMMENDATION ANALYTICS (STEP 17.4)
    # ==========================
    st.markdown("---")
    st.subheader("🧠 Hiring Recommendation Analytics")

    col7, col8 = st.columns(2)

    with col7:
        rec_df = pd.DataFrame(
            analytics["recommendation_distribution"].items(),
            columns=["Recommendation", "Count"]
        )
        fig_rec = px.bar(
            rec_df,
            x="Recommendation",
            y="Count",
            title="Hiring Recommendation Distribution",
            color="Recommendation",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_rec, use_container_width=True)

    with col8:
        action_df = pd.DataFrame(
            analytics["action_distribution"].items(),
            columns=["Action", "Count"]
        )
        fig_action = px.pie(
            action_df,
            names="Action",
            values="Count",
            title="Recommended Hiring Actions"
        )
        st.plotly_chart(fig_action, use_container_width=True)

    # ==========================
    # ROW 5 → SCORE vs RECOMMENDATION
    # ==========================
    score_rec_df = pd.DataFrame(analytics["recommendation_vs_score"])
    fig_score_rec = px.box(
        score_rec_df,
        x="recommendation",
        y="final_score",
        title="Final Score vs Recommendation",
        color="recommendation"
    )
    st.plotly_chart(fig_score_rec, use_container_width=True)

else:
    st.info("⬆️ Upload an ATS Report CSV to view analytics.")
