# AI Resume Screener –  spaCy and Google Cloud Run

An end-to-end application that leverages **Streamlit** as the interactive frontend and **FastAPI** as the robust backend to intelligently screen resumes against job descriptions. This solution is fully containerized using **Docker** and deployed to **Google Cloud Run** for highly scalable, cost-efficient, and serverless performance.

---

##  Live Application

Experience the AI Resume Screener in action!

 [**Launch the App Here!**](https://ai-resume-screener-885446706784.europe-west1.run.app)

---

## Features

*  **Effortless Document Upload:** Easily upload resumes (PDF) and Job Descriptions (PDF).
*  **Intelligent Matching:** Utilizes advanced spaCy models for smart resume-to-JD similarity scoring.
*  **Intuitive User Interface:** Powered by Streamlit for a smooth and interactive user experience.
*  **Robust Backend Logic:** FastAPI handles efficient text extraction, sophisticated similarity scoring, and summarization.
*  **Scalable Cloud Deployment:** Seamlessly deployed on Google Cloud Run, ensuring high availability and auto-scaling.

---

##  Project Structure

```

📦 AI-Resume-Screener/
├── app/                  
│   ├── JDMatcher.py      
│   ├── Scorer.py         
│   ├── TextExtractor.py  
│   ├── Summarize.py      
│   └── main.py           
├── frontend/             
│   └── streamlit_app.py  
├── requirements.txt      
├── Dockerfile            
└── README.md             

````

---

##  Run Locally

Follow these steps to get the AI Resume Screener running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/Dhanraj200547/AI-Resume-Screener.git](https://github.com/Dhanraj200547/AI-Resume-Screener.git)
cd AI-Resume-Screener
````

### 2\. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3\. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4\. Run Both Servers (Locally)

This application requires both the FastAPI backend and Streamlit frontend to run concurrently. Open two separate terminal windows.

**Terminal 1 (For FastAPI Backend):**

```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (For Streamlit Frontend):**

```bash
streamlit run frontend/streamlit_app.py
```

Once both servers are running, open your web browser and navigate to the address provided by Streamlit (usually `http://localhost:8501`).

-----

##  Docker Deployment

This project is designed for unified Docker deployment, running both FastAPI and Streamlit within a single container.

### Dockerfile

Below is the `Dockerfile` used to build the container image:

```dockerfile
# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything from the current directory into the container's /app directory
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the necessary spaCy model
RUN python -m spacy download en_core_web_sm

# Expose port 7860 for Streamlit (as per Cloud Run default for web services)
# Cloud Run expects a single web service on the port specified by the PORT environment variable (default 8080 or custom)
# We map 7860 to the internal Cloud Run PORT later during deployment.
EXPOSE 7860

# Command to run both FastAPI and Streamlit concurrently
# FastAPI runs in the background, Streamlit runs in the foreground.
# The `sleep 3` gives FastAPI a moment to start before Streamlit tries to connect.
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & sleep 3 && streamlit run frontend/streamlit_app.py --server.port 7860 --server.address 0.0.0.0"]
```

-----

##  Requirements

The `requirements.txt` file lists the core Python dependencies:

  * `python-multipart`
  * `scikit-learn`
  * `fastapi`
  * `uvicorn`
  * `streamlit`
  * `requests`
  * `PyMuPDF`
  * `spacy`
  * `en_core_web_sm` (spaCy model - downloaded via command in Dockerfile)

-----

##  Tips for Optimization

For production deployments on Google Cloud Run, consider these best practices:

  * **Streamlit Version:** Ensure you are using Streamlit version `1.19.0` or higher to benefit from improved health check behavior and reduced cold starts.
  * **Docker Image Size:** Utilize `slim` or `alpine` base images in your `Dockerfile` to keep the image size minimal, leading to faster deployments and lower costs.
  * **Cost Control:** Set `min_instances=0` in your Cloud Run service configuration. This allows your application to scale down to zero instances when idle, meaning you only pay when requests are actively being served.
  * **Backend Security:** For enhanced security, consider implementing authentication (e.g., API keys, OAuth) for your FastAPI backend endpoints, especially if they perform sensitive operations or handle private data.
  * **Resource Allocation:** Optimize CPU and memory settings on Cloud Run based on your application's actual needs to further control costs.

-----

##  Future Enhancements

We are continuously working to improve the AI Resume Screener\! Planned enhancements include:

  *  **Advanced AI Ranking:** Integrating more sophisticated AI models for nuanced resume ranking and candidate scoring.
  *  **Automated Candidate Communication:** Features to email shortlisted candidates directly from the application.
  *  **Employer Dashboard:** A dedicated dashboard for employers to manage job postings, view applications, and track screening progress.
  *  **Analytics and Insights:** Providing deeper analytics on resume trends, job description performance, and hiring metrics.

-----

##  Contributing

Contributions are highly encouraged\! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch for your feature or fix.
3.  Submit a pull request.

For major changes, please open an issue first to discuss your proposed changes.

-----

##  Contact

Connect with the creator:

  * **Built by:** [O Dhanraj](https://github.com/Dhanraj200547)
  * **LinkedIn:** [Reach out on LinkedIn](https://www.google.com/search?q=https://www.linkedin.com/in/odeti-dhanraj-2972b3273)
  * **GitHub:** [Explore my other projects on GitHub](https://github.com/Dhanraj200547)

-----

```
```
