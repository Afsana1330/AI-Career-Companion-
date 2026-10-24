
import streamlit as st
from groq import Groq
import os

st.set_page_config(
    page_title="AI Career Companion",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI Career Companion")
st.write(
    "Analyze your resume, identify skill gaps, "
    "and get personalized career guidance with AI."
)

st.divider()

st.header("📄 Resume Analyzer")

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

st.header("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    placeholder="Paste the job requirements here..."
)

if st.button("Analyze My Career", type="primary"):
    if resume_file is None:
        st.warning("Please upload your resume PDF.")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        st.success("Resume and job description received!")
        st.info(
            "Next, we will connect PDF text extraction, "
            "skill gap analysis, and Groq AI."
        )
      
