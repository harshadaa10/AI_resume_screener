# AI Resume Screener (ATS)

**AI-Powered Resume Screening, Ranking & Explainability System**  
A comprehensive resume screening solution that automatically ranks candidate resumes against a job description — with semantic matching, bias analysis, explainable insights, and recruiter override feedback.

---

## 🔍 Overview

Traditional Applicant Tracking Systems rely on keywords and rules, often missing strong candidates due to phrasing differences or bias.  
This project combines **Natural Language Processing (NLP)**, **semantic embeddings**, and **explainable logic** to deliver a fair, transparent, and efficient ATS experience.

✔ Upload PDFs and analyze resumes  
✔ Semantic similarity matching (embeddings)  
✔ Domain & experience evaluation  
✔ Fraud / inflation detection  
✔ Bias fairness analytics  
✔ Human-in-the-loop override & scoring  
✔ Exportable ATS reports  

---

## 📌 Features

### 📥 Input
- Multiple resume upload (.pdf/.txt)
- Job description text input

### 🚀 Scoring & Ranking
- Semantic and rule-based scoring
- Weighted skill/experience/domain importance
- Final ranked list of candidates

### 🧠 Explainability
- Recruiter-friendly explanations
- Strengths & concerns
- Clear verdict categories (Strongly Shortlisted, Shortlisted, Consider with Caution, Not Shortlisted)

### 📊 Analytics
- Bias & fairness metrics
- Score distribution charts
- Summary insights

### 💾 Feedback & Overrides
- Human score adjustment
- Override recommendation
- Recruiter notes saved

### 📁 Reporting
- CSV export of ATS results

---

## 🧠 Technical Architecture

Streamlit UI
│
├── Resume Parsing
├── Embeddings (Semantic similarity)
├── Skill Extraction
├── Experience & Domain Scoring
├── Fraud Detection
├── Bias Analysis
├── Recommendation Engine
├── Explanation Engine
└── Fairness & Feedback Dashboard 

---

## 🛠️ Tech Stack & Dependencies

**Language & Frameworks**
- Python 3.x  
- Streamlit (UI)

**AI & NLP**
- `sentence-transformers` (embeddings)
- Semantic similarity scoring
- Rule + heuristic NLP logic  

**Testing**
- PyTest for unit, integration, pipeline tests

**Libraries**
- pandas, numpy, matplotlib
- pdfplumber, pytesseract (OCR)
- scikit-learn

> Exact versions and dependencies can be found in `requirements.txt`

---


---

## 🛠️ Tech Stack & Dependencies

**Language & Frameworks**
- Python 3.x  
- Streamlit (UI)

**AI & NLP**
- `sentence-transformers` (embeddings)
- Semantic similarity scoring
- Rule + heuristic NLP logic  

**Testing**
- PyTest for unit, integration, pipeline tests

**Libraries**
- pandas, numpy, matplotlib
- pdfplumber, pytesseract (OCR)
- scikit-learn

> Exact versions and dependencies can be found in `requirements.txt`

---


---

## 🛠️ Tech Stack & Dependencies

**Language & Frameworks**
- Python 3.x  
- Streamlit (UI)

**AI & NLP**
- `sentence-transformers` (embeddings)
- Semantic similarity scoring
- Rule + heuristic NLP logic  

**Testing**
- PyTest for unit, integration, pipeline tests

**Libraries**
- pandas, numpy, matplotlib
- pdfplumber, pytesseract (OCR)
- scikit-learn
  
---
🧪 Testing

This project includes automated tests covering:
- Unit tests
- Integration tests
- End-to-end pipeline


