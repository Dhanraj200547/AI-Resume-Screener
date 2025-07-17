# Use a slim Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the entire project
COPY . .

# Expose Streamlit port
EXPOSE 7860

# Run FastAPI in background and launch Streamlit
CMD ["python", "streamlit_app.py"]
