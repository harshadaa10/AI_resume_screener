from experience_engine import extract_experience

def test_experience_extraction():
    text = "Worked as a software engineer for 3 years at Infosys"
    years = extract_experience(text)

    assert years >= 3
