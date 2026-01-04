from resume_fraud_engine import analyze_resume_fraud

def test_fraud_detection_low_risk():
    text = "Built ML pipeline, deployed models, worked on real projects"
    skills = ["python", "machine learning"]

    result = analyze_resume_fraud(text, skills)

    assert result["risk_level"] == "LOW RISK"
    assert result["fraud_score"] < 15
