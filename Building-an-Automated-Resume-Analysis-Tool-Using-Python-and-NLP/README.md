# Building an Automated Resume Analysis Tool Using Python and NLP

## Introduction

Recruitment is a critical process for organizations, but manually reviewing hundreds of resumes is time-consuming, error-prone, and inefficient. Resumes come in various formats, making it challenging to quickly identify relevant skills, qualifications, or experience.

An **automated resume analysis tool** addresses these issues by leveraging **Python** and **Natural Language Processing (NLP)** to parse resumes, extract key information, match them against job descriptions, and rank candidates based on their suitability.

This project guide provides a detailed, step-by-step approach to building such a tool, designed to assist interns in creating a functional and scalable solution. The tool accepts resumes in **PDF or Word formats**, extracts details like **name, email, skills, education**, and **experience**, compares them to a job description, and presents results in a **user-friendly web interface**.

---

## Why Automate Resume Screening?

Manual resume screening poses several challenges:

- **Volume**: Recruiters often handle hundreds or thousands of resumes, leading to fatigue and oversight.
- **Inconsistency**: Resumes lack a standardized format, complicating the identification of key information.
- **Time**: Manual review is slow, delaying the hiring process.
- **Bias and Errors**: Human judgment can introduce biases or miss critical details.

An automated tool streamlines this process by:

- Extracting structured data from unstructured resumes.
- Matching candidates to job requirements objectively.
- Ranking candidates to prioritize the best fits.
- Providing a simple interface for recruiters to review results.

This guide outlines the steps to build such a tool, using **Python** and widely available libraries, ensuring accessibility for interns with basic programming knowledge.

---

## Technologies Used

The project relies on the following technologies:

- **Python**: The primary language for scripting and backend logic.
- **PDFMiner / PyPDF2**: For extracting text from PDF files.
- **python-docx / docx2txt**: For extracting text from Word documents (.docx).
- **SpaCy / NLTK**: For Natural Language Processing and named entity recognition.
- **Scikit-learn**: For implementing TF-IDF vectorization and cosine similarity.
- **Streamlit**: To create a web interface. Alternatives include **Flask** for custom UIs.

All tools are open-source and well-documented.

---

## Step-by-Step Guide to Building the Tool

### Step 1: Accepting and Reading Resumes

#### Setting Up the Web Interface

- Use **Streamlit** to allow resume uploads via `st.file_uploader`.
- Accept `.pdf` and `.docx` files.
- Enable multiple file uploads.
- Add a text area for job description input.

#### Determining File Type

- Use file extension to detect format (`.pdf` or `.docx`).

#### Extracting Text

- **PDFs**: Use PDFMiner for complex PDFs or PyPDF2 for simpler ones.
- **Word Docs**: Use `python-docx` for structured content or `docx2txt` for plain text.

#### Storing Extracted Text

- Store text in variables or dictionaries, tagged by filename or candidate ID.

---

### Step 2: Extracting Key Information

#### Name and Contact Info

- **Name**: Use SpaCy NER or regex for capitalized name patterns.
- **Email**: Regex: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- **Phone**: Regex: `(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}`

#### Skills

- Match against a predefined skill list using string matching or tokenization.
- Advanced: Train a custom SpaCy NER model.

#### Education

- Look for keywords like "Education" or "Academic Background".
- Regex for degrees + years (e.g., `Bachelor.*\d{4}`)
- Use SpaCy for recognizing institutions and years.

#### Experience

- Use keywords like "Work History".
- Regex patterns for job roles and durations (e.g., `.*Engineer.*\d{4}-\d{4}`)
- Calculate years of experience from date ranges.

---

### Step 3: Matching with Job Description

#### Text Preprocessing

- Lowercase all text.
- Remove punctuation, stop words.
- Lemmatize words.
- Use SpaCy or NLTK for preprocessing.

#### TF-IDF Vectorization

- Use `TfidfVectorizer` from Scikit-learn.
- Generate vectors for each resume and job description.

#### Cosine Similarity

- Use `cosine_similarity` to compare resumes to job descriptions.
- Scores close to 1 mean stronger matches.

---

### Step 4: Ranking Candidates

- Store similarity scores for each resume.
- Sort in descending order.
- Apply optional threshold (e.g., 0.7).
- Organize results with names, scores, emails, top skills.

---

### Step 5: Frontend Interface

Build with **Streamlit**:

- Resume uploader
- Job description text input
- Table showing:
  - Name
  - Email
  - Skills
  - Similarity Score
  - Resume filename or download link
- Score filtering using slider

Use `st.dataframe` for display and `st.button` to trigger processing.

---

## Additional Considerations

- **Error Handling**: Show messages for invalid files, missing data, unreadable content.
- **Scalability**: Use multiprocessing or batch jobs for large uploads.
- **Customization**: Let users modify skill lists or job criteria.
- **Testing**: Try with varied resumes and verify accuracy.

---

## Benefits of the Tool

- ✅ **Efficiency**: Saves time on screening.
- ✅ **Accuracy**: Objectively matches job profiles.
- ✅ **Ease of Use**: Minimal training needed.
- ✅ **Scalability**: Works with many resumes.
- ✅ **Customizability**: Adapts to industries or job types.

---

## Conclusion

Building an automated resume analysis tool combines **Python**, **NLP**, and **web development**. This guide walks you through:

1. Uploading resumes
2. Extracting structured info
3. Matching to job descriptions
4. Ranking candidates
5. Displaying results in a web app

Enhancements like OCR, HR integrations, and batch processing can be added later. Thoroughly test your implementation to ensure robustness.

---

## Resources

### GitHub Repositories

- [OmkarPathak/ResumeParser](https://github.com/OmkarPathak/ResumeParser)
- [sanketsarwade/Resume-Parser-using-Python](https://github.com/sanketsarwade/Resume-Parser-using-Python)
- [kbrajwani/resume_parser](https://github.com/kbrajwani/resume_parser)
- [hxu296/nlp-resume-parser](https://github.com/hxu296/nlp-resume-parser)
- [bjherger/ResumeParser](https://github.com/bjherger/ResumeParser)

### Tutorials & Articles

- [How to build a Resume Parser using Python (GeeksforGeeks)](https://www.geeksforgeeks.org/nlp/project-how-to-build-a-resume-parser-using-python/)
- [NER in Python with SpaCy (Analytics Vidhya)](https://www.analyticsvidhya.com/blog/2021/06/nlp-application-named-entity-recognition-ner-in-python-with-spacy/)
- [Training Custom NER in SpaCy (Machine Learning Plus)](https://www.machinelearningplus.com/nlp/training-custom-ner-model-in-spacy/)
- [TF-IDF Cosine Similarity (Stack Overflow)](https://stackoverflow.com/questions/12118720/python-tf-idf-cosine-to-find-document-similarity)
- [TF-IDF and similarity scores (Chan’s Notebook)](https://colab.research.google.com/github/goodboychan/chans_jupyter/blob/main/_notebooks/2020-07-17-04-TF-IDF-and-similarity-scores.ipynb)
- [Streamlit file_uploader (Forum)](https://discuss.streamlit.io/t/file-uploading-and-reading-using-st-file-uploader/31897)
- [Working with File Uploads (JCharisTech)](https://blog.jcharistech.com/2020/11/08/working-with-file-uploads-in-streamlit-python/)

### YouTube Tutorials

- Search for:
  - "Spacy 3 Masterclass Tutorials"
  - "How to Build Resume Parser with NLP"
  - "TF-IDF Cosine Similarity Python Tutorials"
  - "Streamlit st.file_uploader usage"

### Additional Cosine Similarity Resources

- [How to Calculate Cosine Similarity Using TF-IDF (ML Journey)](https://mljourney.com/how-to-calculate-cosine-similarity-using-tf-idf/)
- [TF-IDF and Similarity Scores (Kakamana Blog)](https://kakamana.github.io/posts/TF-IDF%20and%20similarity%20scores/TF-IDF%20and%20similarity%20scores.html)
