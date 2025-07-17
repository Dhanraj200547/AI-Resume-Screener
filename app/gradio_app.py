import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/analyze/"

def analyze_resume(resume_file, jd_file):
    if resume_file is None or jd_file is None:
        return "Please upload both files.", None, None

    files = {
        "resume": resume_file,
        "jd": jd_file
    }

    try:
        response = requests.post(API_URL, files=files)
        if response.status_code == 200:
            result = response.json()
            match_score = f"{result['match']}%"
            ats_score = f"{result['score']}%"
            summary = result["summary"]
            return f"✅ Match Score: {match_score}", ats_score, summary
        else:
            return "❌ Error: Could not analyze resume.", "", ""
    except Exception as e:
        return f"❌ Exception: {str(e)}", "", ""

# Build the UI
resume_input = gr.File(label="Upload Resume (PDF)", type="binary")
jd_input = gr.File(label="Upload Job Description (PDF)", type="binary")

match_score_output = gr.Textbox(label="Match Score")
ats_score_output = gr.Textbox(label="ATS Score")
summary_output = gr.JSON(label="Resume Summary")

interface = gr.Interface(
    fn=analyze_resume,
    inputs=[resume_input, jd_input],
    outputs=[match_score_output, ats_score_output, summary_output],
    title="AI Resume Screener (Gradio)",
    description="Upload a resume and job description to check ATS score and match percentage."
)

if __name__ == "__main__":
    interface.launch()
