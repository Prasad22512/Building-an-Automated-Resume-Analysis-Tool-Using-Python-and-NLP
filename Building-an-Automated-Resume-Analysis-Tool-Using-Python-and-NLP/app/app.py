import streamlit as st
from pathlib import Path
import re
import json
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pprint import pprint
from pathlib import Path




# Load NLP model and skill list
nlp = spacy.load("en_core_web_sm")
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to resume-analyzer/
SKILLS_PATH = BASE_DIR / "data" / "skills.json"
with open(SKILLS_PATH) as f:
    skill_list = json.load(f)


# Helper functions from Notebook 2
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else None

def extract_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:5]:
        if "@" not in line and not re.search(r"\d", line):
            if 2 <= len(line.split()) <= 4:
                return line
    return None

def extract_skills(text, skills):
    tokens = [token.text.lower() for token in nlp(text)]
    found = [skill for skill in skills if skill.lower() in tokens]
    return list(set(found))

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)

def extract_text_from_file(uploaded_file):
    from PyPDF2 import PdfReader
    import docx

    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "pdf":
        reader = PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""
st.title("📄 Resume Scorer App")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_desc = st.text_area("Paste Job Description Here")

if st.button("Process"):
    if uploaded_files and job_desc:
        profiles = []
        resume_texts = []

        for file in uploaded_files:
            text = extract_text_from_file(file)
            resume_texts.append((file.name, text))

            profile = {
                "filename": file.name,
                "name": extract_name(text),
                "email": extract_email(text),
                "phone": extract_phone(text),
                "skills": extract_skills(text, skill_list),
                "text": text  # Save for similarity
            }
            profiles.append(profile)

        # Preprocess text
        jd_clean = preprocess(job_desc)
        resumes_clean = [preprocess(p["text"]) for p in profiles]

        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(resumes_clean + [jd_clean])
        jd_vector = tfidf_matrix[-1]
        resume_vectors = tfidf_matrix[:-1]

        # Similarity scores
        scores = cosine_similarity(resume_vectors, jd_vector).flatten()
        for i, score in enumerate(scores):
            profiles[i]["similarity"] = round(float(score), 3)

        # Sort profiles by score
        ranked = sorted(profiles, key=lambda x: x["similarity"], reverse=True)

        # Display results
        st.subheader("📊 Ranked Candidates")
        for r in ranked:
            st.markdown(f"""
            **🧑 Name:** {r.get('name', 'N/A')}  
            **📧 Email:** {r.get('email', 'N/A')}  
            **📱 Phone:** {r.get('phone', 'N/A')}  
            **🛠️ Skills:** {', '.join(r.get('skills', []))}  
            **📈 Match Score:** `{r['similarity']}`
            ---
            """)
    else:
        st.warning("Please upload at least one resume and paste a job description.")
