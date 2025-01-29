# GCP FastAPI API

A **FastAPI**-based service that demonstrates how to:

- Read and write **Firestore** documents  
- Upload/download files from **Google Cloud Storage**  
- Publish messages to **Google Pub/Sub**  

This project can be run locally using Docker or deployed to **Google Cloud Run** for a fully managed serverless experience.

---

## Features

1. **Firestore**: Create and fetch documents from a specified Firestore collection.  
2. **Cloud Storage**: Upload and download files to/from a GCS bucket.  
3. **Pub/Sub**: Publish messages to a configured Pub/Sub topic.  
4. **FastAPI Documentation**: Automatic OpenAPI/Swagger UI at `/docs`.

---

## Prerequisites

1. **Python 3.9+** (if running locally without Docker)  
2. **Docker** (for containerized deployments)  
3. **A GCP Project** with:
   - **Firestore** enabled  
   - A **GCS bucket**  
   - A **Pub/Sub** topic  
4. **Service Account Credentials** (optional if developing locally with Docker):  
   - You must either provide a **service account JSON** containing the `project_id` or explicitly set the project ID in code.  

---

## Installation (Local Python Environment)

*(Skip this section if you’re only running via Docker.)*

```bash
# Clone this repository
git clone https://github.com/your-org/gcp-fastapi-api.git
cd gcp-fastapi-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
