import streamlit as st
from dotenv import load_dotenv
from parser import parse_pdf, parse_docx, parse_url
from llm import rate_resume

load_dotenv()
st.set_page_config(page_title="Resume Rater", layout="centered")
st.title("Resume Rater")

st.subheader("Company Name")
company_name = st.text_input("Enter the company name")

# ----------Job Description----------
st.subheader("Job Description")
jd_type = st.radio("Input Type", ["Text", "File", "URL"])

jd_text = ""

if jd_type == "Text":
    jd_text = st.text_area("Enter the job description", height=200)

elif jd_type == "URL":
    url = st.text_input("Enter the URL")
    if url:
        jd_text = parse_url(url)

else:
    jd_file = st.file_uploader("Upload a job description", type=["pdf", "docx"])
    if jd_file:
        jd_text = parse_pdf(jd_file) if jd_file.type == "application/pdf" else parse_docx(jd_file)

# ----------Resume----------

st.subheader("Resume")
resume_file = st.file_uploader("Upload a resume", type=["pdf", "docx"])

resume_text = ""
if resume_file:
    resume_text = parse_pdf(resume_file) if resume_file.type == "application/pdf" else parse_docx(resume_file)

# ----------Rate Resume----------
if st.button("Rate Resume"):
    if not jd_text or not resume_text:
        st.error("Please fill in all fields")
    else:
        with st.spinner("Rating resume..."):
            try:
                result = rate_resume(company_name, jd_text, resume_text)
                
                overall_score = result.get("overall_score", "N/A")
                st.success(f"Resume score: {overall_score}")

                st.subheader("Strengths")
                for s in result.get("strengths", []):
                    st.write("•", s)

                st.subheader("Gaps")
                for g in result.get("gaps", []):
                    st.write("•", g)

                st.subheader("Improvements")
                for i in result.get("improvements", []):
                    st.write("•", i)
            except Exception as e:
                st.error(f"Error rating resume: {str(e)}")
                st.json(result if 'result' in locals() else {})
    
