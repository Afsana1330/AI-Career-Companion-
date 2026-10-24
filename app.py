
import os
import streamlit as st
from groq import Groq
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Career Companion",
    page_icon="🚀"
)

st.title("🚀 AI Career Companion")
st.write("AI-powered Resume Analysis and Career Guidance")

resume_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=200
)

if st.button("Analyze My Career", type="primary"):

    if resume_file is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            reader = PdfReader(resume_file)
            resume_text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

            if not resume_text.strip():
                st.error("Could not extract text from this PDF.")
                st.stop()

            api_key = st.secrets.get("GROQ_API_KEY", "")

            if not api_key:
                st.error("Groq API key is missing from Secrets.")
                st.stop()

            with st.spinner("AI is analyzing your resume..."):
                client = Groq(api_key=api_key)

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI career advisor. "
                                "Compare the resume with the job description. "
                                "Identify matching skills, missing skills, "
                                "strengths, improvement areas, and suitable "
                                "learning steps. Suggest interview questions. "
                                "Use simple English. Do not invent qualifications "
                                "or experience."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                "RESUME:\n"
                                + resume_text[:12000]
                                + "\n\nJOB DESCRIPTION:\n"
                                + job_description[:8000]
                            )
                        }
                    ],
                    max_tokens=1200,
                    temperature=0.2
                )

                report = response.choices[0].message.content

            st.subheader("📊 Your AI Career Report")
            st.markdown(report)

            st.download_button(
                "📥 Download Report",
                data=report,
                file_name="AI_Career_Report.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(
                "Analysis failed. Please check your API configuration "
                "and try again."
            )
            st.caption(f"Error details: {e}")
            
