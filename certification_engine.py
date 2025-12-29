# certification_engine.py

CERTIFICATIONS = {
    "HR": ["shrm", "shrm-cp", "phr", "sphr"],
    "Information-Technology": ["aws", "azure", "gcp", "ccna", "cissp"],
    "Management": ["pmp", "prince2"],
    "Finance": ["cfa", "frm"],
    "Construction": ["pmp", "autocad certified"]
}

def extract_certifications(text):
    text = text.lower()
    found = []

    for certs in CERTIFICATIONS.values():
        for cert in certs:
            if cert in text:
                found.append(cert.upper())

    return list(set(found))


def certification_score(jd_text, resume_text):
    jd_certs = extract_certifications(jd_text)
    resume_certs = extract_certifications(resume_text)

    boost = 0

    for cert in resume_certs:
        if cert.lower() in [c.lower() for c in jd_certs]:
            boost += 10
        else:
            boost += 5

    return boost, resume_certs
