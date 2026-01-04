from ranking_engine import rank_resumes

def test_end_to_end_resume_screening():
    results = rank_resumes(
        resume_folder="data/test_resumes_unit",
        jd_text="Looking for Python ML engineer",
        weights={
    "skill": 1.0,
    "experience": 1.0,
    "cert": 1.0,
    "domain_penalty": 1.0
}

    )

    assert len(results) > 0
    assert "final_score" in results[0]
    assert "verdict" in results[0]
