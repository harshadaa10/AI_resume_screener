from ranking_engine import rank_resumes
import pandas as pd
from summary_engine import generate_summary

# ==========================
# CONFIG
# ==========================
TEST_RESUME_FOLDER = "data/test_resumes"
STORED_RESUME_FOLDER = "data/stored_resumes"
JD_PATH = "data/job_description.txt"


def main():
    print("AI Resume Screener Project Started Successfully!\n")

    # ==========================
    # LOAD JOB DESCRIPTION
    # ==========================
    with open(JD_PATH, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # ==========================
    # 🔁 CHOOSE MODE
    # ==========================
    MODE = "test"   # change to "test" if needed

    if MODE == "test":
        resume_folder = TEST_RESUME_FOLDER
    else:
        resume_folder = STORED_RESUME_FOLDER

    # ==========================
    # RUN ATS ENGINE
    # ==========================
    ranked_results = rank_resumes(
        resume_folder=resume_folder,
        jd_text=jd_text,
        mode=MODE
    )

    # ==========================
    # GENERATE SUMMARY
    # ==========================
    summary = generate_summary(ranked_results)
    print("\n📊 ATS SUMMARY REPORT\n")
    print(f"Total Resumes Processed : {summary['total_resumes']}")
    print(f"Average ATS Score       : {summary['average_score']} %")
    print(f"Best Candidate          : {summary['best_candidate']}")
    print(f"Consider Count          : {summary['consider_count']}")
    print(f"Reject Count            : {summary['reject_count']}")
    print("=" * 60)

    # ==========================
    # DISPLAY RANKED RESUMES
    # ==========================
    print("\n🏆 Final ATS Resume Ranking:\n")

    for idx, res in enumerate(ranked_results, start=1):
        print(f"{idx}. {res['resume']}")
        print(f"   Base Similarity : {res['base_score']} %")
        print(f"   Skill Boost     : +{res['boost']}")
        print(f"   Penalty         : -{res['penalty']}")
        print(f"   Final Score     : {res['final_score']} %")
        print(f"   Resume Domain   : {res['resume_domain']}")
        print(f"   JD Domain       : {res['jd_domain']}")
        print(f"   Confidence      : {res['confidence']}")
        print(f"   ✔ Matched Skills: {res['matched_skills']}")
        print(f"   ✖ Missing Skills: {res['missing_skills']}")
        print("-" * 60)

    # ==========================
    # EXPORT ATS REPORT
    # ==========================
    df = pd.DataFrame(ranked_results)
    report_name = f"ats_report_{MODE}.csv"
    df.to_csv(report_name, index=False)
    print(f"\n📁 ATS Report saved successfully as: {report_name}")


if __name__ == "__main__":
    main()
