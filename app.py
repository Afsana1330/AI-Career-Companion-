
import os
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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

            pdf_buffer = BytesIO()

            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            styles = getSampleStyleSheet()

            story = []

            story.append(Paragraph(
                "AI CAREER COMPANION REPORT",
                styles["Title"]
            ))

            story.append(Spacer(1, 20))

            report_content = escape(report).replace(
                "\n", "<br/>"
            )

            body_style = ParagraphStyle(
                "Report",
                parent=styles["Normal"],
                fontSize=10,
                leading=15
            )

            story.append(
                Paragraph(report_content, body_style)
            )

            doc.build(story)

            pdf_buffer.seek(0)

            st.download_button(
                "📥 Download PDF Report",
                data=pdf_buffer.getvalue(),
                file_name="AI_Career_Report.pdf",
                mime="application/pdf"
           )