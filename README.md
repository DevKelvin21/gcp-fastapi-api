# GCP FastAPI API

A **FastAPI**-based service that demonstrates how to:

- Read and write **Firestore** documents  
- Upload/download files from **Google Cloud Storage**  
- Publish messages to **Google Pub/Sub**  
- Authenticate users via **Google OAuth 2.0**  

This project can be run locally using Docker or deployed to **Google Cloud Run** for a fully managed serverless experience.

---

## 🛠️ **Features**

1. **Architectural Enhancements:**
   - **Separation of Concerns:** Business logic is modularized into dedicated service layers (`firestore_service.py`, `pubsub_service.py`, `storage_service.py`).
   - **Organized Project Structure:** Clear directories for models, routers, and services to promote maintainability.

2. **Firestore Integration:**
   - **CRUD Operations:** Create, retrieve, update, and delete documents from a specified Firestore collection.
   - **API Endpoints:** Managed under `/firestore` for seamless interaction.

3. **Pub/Sub Integration:**
   - **Messaging:** Publish messages to configured Pub/Sub topics.
   - **API Endpoints:** Managed under `/pubsub` for efficient message handling.

4. **Cloud Storage Integration:**
   - **File Handling:** Upload and download files to/from a designated GCS bucket.
   - **API Endpoints:** Managed under `/storage` for streamlined file operations.

5. **Authentication:**
   - **Google OAuth 2.0:** Secure API endpoints with Google Sign-In.
   - **Dependency Injection:** Implemented using Pydantic models and Firestore for allowed client IDs.

6. **API Documentation:**
   - **Interactive Interface:** Access Swagger UI at `/docs` for comprehensive API exploration.

7. **Docker Configuration:**
   - **Optimized Dockerfile:** Uses Python 3.12-slim base image, installs dependencies globally, and runs as a non-root user.
   - **Security Enhancements:** Mounts service account credentials securely and exposes necessary ports.

---

## 📋 **Prerequisites**

1. **Python 3.12+** (if running locally without Docker)  
2. **Docker** (for containerized deployments)  
3. **A GCP Project** with:
   - **Firestore** enabled  
   - A **GCS bucket**  
   - A **Pub/Sub** topic  
4. **Service Account Credentials** (for non-local deployments):
   - A **service account JSON** with permissions for Firestore, Pub/Sub, and Cloud Storage.
5. **Google OAuth 2.0 Credentials**:
   - A **Google OAuth Client ID** for authentication.

---

## 📂 **Project Structure**

```
gcp-fastapi-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth_google.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── claims.py
│   │   └── item.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── firestore.py
│   │   ├── pubsub.py
│   │   └── storage.py
│   └── services/
│       ├── __init__.py
│       ├── firestore_service.py
│       ├── pubsub_service.py
│       └── storage_service.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## 🚀 **Installation**

### 🐳 **Using Docker**

1. **Build the Docker Image:**

   ```bash
   docker build -t gcp-fastapi-api:latest .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 8080:8080 \
     -e FIRESTORE_COLLECTION="your-firestore-collection" \
     -e BUCKET_NAME="your-gcs-bucket-name" \
     -e PUBSUB_TOPIC="projects/your-gcp-project-id/topics/your-pubsub-topic" \
     -e GOOGLE_APPLICATION_CREDENTIALS="/app/creds/service-account.json" \
     -v /path/on/host/service-account.json:/app/creds/service-account.json:ro \
     gcp-fastapi-api:latest
   ```

   **Notes:**

   - **Environment Variables (`-e`):** Pass necessary environment variables to the container.
   - **Volume Mount (`-v`):** Mount the service account JSON file into the container at `/app/creds/service-account.json`.
   - **Ports (`-p`):** Maps port `8080` in the container to port `8080` on the host.

3. **Access the Application:**

   - **Health Check:**
     
     ```bash
     curl http://localhost:8080/health
     ```

     **Expected Response:**

     ```json
     {
       "status": "OK"
     }
     ```

   - **API Documentation:**
     
     Visit [http://localhost:8080/docs](http://localhost:8080/docs) to access the Swagger UI and interact with your API endpoints.

### 🐍 **Running Locally with Python**

*(Skip this section if you’re only running via Docker.)*

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-org/gcp-fastapi-api.git
   cd gcp-fastapi-api
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or on Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the project root with the following content:

   ```env
   FIRESTORE_COLLECTION="your-firestore-collection"
   BUCKET_NAME="your-gcs-bucket-name"
   PUBSUB_TOPIC="projects/your-gcp-project-id/topics/your-pubsub-topic"
   GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
   ```

   **Notes:**

   - **`GOOGLE_APPLICATION_CREDENTIALS`:** Path to your service account JSON file.
   - Ensure that the service account has the necessary permissions for Firestore, Pub/Sub, and Cloud Storage.

5. **Run the Application:**

   ```bash
   uvicorn app.main:app --reload
   ```

   **Or:**

   ```bash
   python -m app.main
   ```

6. **Access the Application:**

   - **Health Check:**
     
     ```bash
     curl http://127.0.0.1:8000/health
     ```

     **Expected Response:**

     ```json
     {
       "status": "OK"
     }
     ```

   - **API Documentation:**
     
     Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the Swagger UI.

---

## 🧩 **Usage**

### 🔑 **Authentication**

This API uses **Google OAuth 2.0** for authentication. To access secured endpoints:

1. **Obtain a Google ID Token:**
   
   - Use your front-end application to sign in with Google and obtain an ID token.

2. **Include the ID Token in Requests:**
   
   - Add the token to the `Authorization` header as a Bearer token:

     ```
     Authorization: Bearer <YOUR_GOOGLE_ID_TOKEN>
     ```

### 🗃️ **Firestore Endpoints**

- **Create Document:**
  
  ```http
  POST /firestore/create
  ```
  
  **Body:**
  
  ```json
  {
    "file_name": "data.csv",
    "uploaded_by_user_id": "user123",
    "phone_columns": ["phone1", "phone2"],
    "column_aliases": {"phone1": "Phone Number 1", "phone2": "Phone Number 2"},
    "phone_column_indexes": [0, 1],
    "phone_order_indexes": [1, 0],
    "has_header_row": true,
    "timestamp": "2023-10-29T12:34:56Z",
    "status": {
      "stage": "uploaded",
      "last_updated": "2023-10-29T12:34:56Z"
    },
    "output_files": {
      "clean_file_path": "clean_data.csv",
      "invalid_file_path": "invalid_data.csv",
      "dnc_file_path": "dnc_data.csv"
    }
  }
  ```

- **Get Document:**
  
  ```http
  GET /firestore/{doc_id}
  ```

- **Update Document:**
  
  ```http
  PUT /firestore/{doc_id}
  ```

  **Body:** *(Same as Create Document)*

- **Delete Document:**
  
  ```http
  DELETE /firestore/{doc_id}
  ```

### 🗄️ **Cloud Storage Endpoints**

- **Upload File:**
  
  ```http
  POST /storage/upload
  ```
  
  **Form Data:**
  
  - `file`: The file to upload.

- **Download File:**
  
  ```http
  GET /storage/download/{file_name}
  ```

### 📢 **Pub/Sub Endpoints**

- **Publish Message:**
  
  ```http
  POST /pubsub/publish
  ```
  
  **Body:**
  
  ```json
  {
    "message": "Your message here"
  }
  ```

---

## 🛠️ **Configuration**

### 📄 **Environment Variables**

Ensure the following environment variables are set either in your `.env` file (for local development) or passed as environment variables in Docker or Cloud Run:

- **`GOOGLE_CLIENT_ID`**: Your Google OAuth Client ID.
- **`GCP_PROJECT_ID`**: Your Google Cloud Project ID.
- **`FIRESTORE_COLLECTION`**: The Firestore collection name.
- **`BUCKET_NAME`**: The name of your Google Cloud Storage bucket.
- **`PUBSUB_TOPIC`**: The Pub/Sub topic to publish messages to (e.g., `projects/your-project-id/topics/your-topic`).
- **`GOOGLE_APPLICATION_CREDENTIALS`**: Path to your service account JSON file inside the container (e.g., `/app/creds/service-account.json`).

### 🛡️ **Service Account Setup**

1. **Create a Service Account:**
   
   - Navigate to the [GCP Console](https://console.cloud.google.com/iam-admin/serviceaccounts).
   - Create a new service account with roles:
     - **Firestore Admin**
     - **Pub/Sub Publisher**
     - **Storage Admin**

2. **Generate and Download JSON Key:**
   
   - After creating the service account, generate a JSON key.
   - Download the key and store it securely on your host machine.

3. **Mount the Service Account Key in Docker:**
   
   - Use the `-v` flag to mount the JSON key into the Docker container as shown in the **Installation** section.

### 🔑 **Google OAuth 2.0 Setup**

1. **Create OAuth Credentials:**
   
   - Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
   - Create an OAuth 2.0 Client ID.
   - Note the **Client ID**, which will be used in your environment variables.

2. **Configure Authorized Redirect URIs:**
   
   - Ensure that your application’s redirect URIs are correctly set to handle OAuth responses.

---

## 📦 **Docker Configuration**

Your current `Dockerfile` has been optimized for the latest Python version and security best practices.

### **Updated `Dockerfile`:**

```dockerfile
# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to ensure output is flushed
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies globally
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Create a non-root user for better security
RUN useradd -m appuser

# Change ownership of the /app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose port 8080 for Cloud Run (or any other target environment)
EXPOSE 8080

# Command to run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### **Explanation of Changes:**

1. **Base Image Updated to Python 3.12:**
   
   ```dockerfile
   FROM python:3.12-slim
   ```
   
   - **Why:** Aligns the Docker environment with the Python version used in development (Python 3.12.2), reducing compatibility issues.

2. **Environment Variables:**
   
   ```dockerfile
   ENV PYTHONUNBUFFERED=1 \
       PYTHONDONTWRITEBYTECODE=1
   ```
   
   - **`PYTHONUNBUFFERED=1`:** Ensures that Python outputs are immediately flushed to the terminal, useful for real-time logging.
   - **`PYTHONDONTWRITEBYTECODE=1`:** Prevents Python from writing `.pyc` files to disk, saving space.

3. **Working Directory:**
   
   ```dockerfile
   WORKDIR /app
   ```
   
   - **Why:** Sets `/app` as the working directory inside the Docker container. All subsequent commands are run from this directory.

4. **System Dependencies Installation:**
   
   ```dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends \
       build-essential \
       && rm -rf /var/lib/apt/lists/*
   ```
   
   - **`build-essential`:** Installs essential build tools required for compiling certain Python packages.
   - **`--no-install-recommends`:** Minimizes the number of packages installed, reducing the final image size.
   - **Cleanup:** Removes the package lists to further reduce the image size.

5. **Python Dependencies Installation:**
   
   ```dockerfile
   COPY requirements.txt /app/
   RUN pip install --upgrade pip
   RUN pip install --no-cache-dir -r requirements.txt
   ```
   
   - **Why:** 
     - Copies `requirements.txt` to leverage Docker's caching mechanism.
     - Upgrades `pip` to the latest version.
     - Installs Python dependencies globally without the `--user` flag, ensuring executables like `uvicorn` are accessible system-wide.

6. **Application Code Copy:**
   
   ```dockerfile
   COPY . /app
   ```
   
   - **Why:** Copies the entire application code into the Docker container.

7. **Non-Root User Setup:**
   
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```
   
   - **Why:** Enhances security by running the application as a non-root user.

8. **File Ownership:**
   
   ```dockerfile
   RUN chown -R appuser:appuser /app
   ```
   
   - **Why:** Ensures that `appuser` has the necessary permissions to access and execute files within `/app`.

9. **Port Exposure and Command:**
   
   ```dockerfile
   EXPOSE 8080
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```
   
   - **Why:** 
     - Exposes port `8080` for Cloud Run or other deployment environments.
     - Starts the FastAPI application using Uvicorn, pointing to the correct application instance (`app.main:app`).

---

## 📝 **Running the Application Locally**

1. **Build the Docker Image:**

   ```bash
   docker build -t gcp-fastapi-api:latest .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 8080:8080 \
     -e FIRESTORE_COLLECTION="your-collection" \
     -e BUCKET_NAME="your-bucket" \
     -e PUBSUB_TOPIC="projects/your-project-id/topics/your-topic" \
     -e GOOGLE_APPLICATION_CREDENTIALS="/app/creds/service-account.json" \
     -v /user-path/keys/service-account.json:/app/creds/service-account.json:ro \
     gcp-fastapi-api:latest
   ```

   **Error Encountered:**

   ```
   /usr/local/bin/python3.12: can't open file '/root/.local/bin/uvicorn': [Errno 13] Permission denied
   ```

   **Resolution:**

   The error indicates a permission issue with accessing the `uvicorn` executable. This is resolved in the updated `Dockerfile` by installing `uvicorn` globally and ensuring the application runs as a non-root user with appropriate permissions.

3. **Verify the Application:**

   - **Health Check:**
     
     ```bash
     curl http://localhost:8080/health
     ```

     **Expected Response:**

     ```json
     {
       "status": "OK"
     }
     ```

   - **API Documentation:**
     
     Visit [http://localhost:8080/docs](http://localhost:8080/docs) to access the Swagger UI and interact with your API endpoints.

---

## 📦 **Docker Configuration**

Your current `Dockerfile` has been updated to align with best practices and resolve permission issues related to `uvicorn`. Here's the final version:

```dockerfile
# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to ensure output is flushed
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies globally
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Create a non-root user for better security
RUN useradd -m appuser

# Change ownership of the /app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose port 8080 for Cloud Run (or any other target environment)
EXPOSE 8080

# Command to run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### **Key Changes Explained:**

1. **Base Image Updated to Python 3.12:**
   
   ```dockerfile
   FROM python:3.12-slim
   ```
   
   - **Why:** Aligns the Docker environment with the Python version used in development (Python 3.12.2), reducing compatibility issues.

2. **Environment Variables:**
   
   ```dockerfile
   ENV PYTHONUNBUFFERED=1 \
       PYTHONDONTWRITEBYTECODE=1
   ```
   
   - **`PYTHONUNBUFFERED=1`:** Ensures that Python outputs are immediately flushed to the terminal, useful for real-time logging.
   - **`PYTHONDONTWRITEBYTECODE=1`:** Prevents Python from writing `.pyc` files to disk, saving space.

3. **Working Directory:**
   
   ```dockerfile
   WORKDIR /app
   ```
   
   - **Why:** Sets `/app` as the working directory inside the Docker container. All subsequent commands are run from this directory.

4. **System Dependencies Installation:**
   
   ```dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends \
       build-essential \
       && rm -rf /var/lib/apt/lists/*
   ```
   
   - **`build-essential`:** Installs essential build tools required for compiling certain Python packages.
   - **`--no-install-recommends`:** Minimizes the number of packages installed, reducing the final image size.
   - **Cleanup:** Removes the package lists to further reduce the image size.

5. **Python Dependencies Installation:**
   
   ```dockerfile
   COPY requirements.txt /app/
   RUN pip install --upgrade pip
   RUN pip install --no-cache-dir -r requirements.txt
   ```
   
   - **Why:** 
     - Copies `requirements.txt` to leverage Docker's caching mechanism.
     - Upgrades `pip` to the latest version.
     - Installs Python dependencies globally without the `--user` flag, ensuring executables like `uvicorn` are accessible system-wide.

6. **Application Code Copy:**
   
   ```dockerfile
   COPY . /app
   ```
   
   - **Why:** Copies the entire application code into the Docker container.

7. **Non-Root User Setup:**
   
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```
   
   - **Why:** Enhances security by running the application as a non-root user.

8. **File Ownership:**
   
   ```dockerfile
   RUN chown -R appuser:appuser /app
   ```
   
   - **Why:** Ensures that `appuser` has the necessary permissions to access and execute files within `/app`.

9. **Port Exposure and Command:**
   
   ```dockerfile
   EXPOSE 8080
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```
   
   - **Why:** 
     - Exposes port `8080` for Cloud Run or other deployment environments.
     - Starts the FastAPI application using Uvicorn, pointing to the correct application instance (`app.main:app`).

### **Ensure Correct Application Reference:**

In your `CMD` instruction:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

- **`app.main:app`:** 
  - **`app.main`:** Refers to the `main.py` file inside the `app/` directory.
  - **`app`:** Refers to the FastAPI instance inside `main.py`.

Ensure that your project structure aligns with this reference:

```
gcp-fastapi-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth_google.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── claims.py
│   │   └── item.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── firestore.py
│   │   ├── pubsub.py
│   │   └── storage.py
│   └── services/
│       ├── __init__.py
│       ├── firestore_service.py
│       ├── pubsub_service.py
│       └── storage_service.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## 📂 **.dockerignore File**

To optimize your Docker build process and reduce the final image size, create a `.dockerignore` file in your project root with the following content:

```gitignore
# Exclude Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd

# Exclude environment variables
.env

# Exclude version control
.git
.gitignore

# Exclude Docker-related files
Dockerfile
docker-compose.yml

# Exclude documentation and miscellaneous files
*.md
```

**Why:** This ensures that unnecessary files and directories are not copied into the Docker image, making the build process faster and the image smaller.

---

## 🔄 **Rebuild and Test Your Docker Image**

After updating your `Dockerfile`, follow these steps to rebuild and test your Docker image:

1. **Build the Docker Image:**

   ```bash
   docker build -t gcp-fastapi-api:latest .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 8080:8080 \
     -e FIRESTORE_COLLECTION="your-collection" \
     -e BUCKET_NAME="your-bucket" \
     -e PUBSUB_TOPIC="projects/your-project-id/topics/your-topic" \
     -e GOOGLE_APPLICATION_CREDENTIALS="/app/creds/service-account.json" \
     -v /user-path/keys/service-account.json:/app/creds/service-account.json:ro \
     gcp-fastapi-api:latest
   ```

3. **Verify the Application:**

   - **Health Check:**
     
     ```bash
     curl http://localhost:8080/health
     ```

     **Expected Response:**

     ```json
     {
       "status": "OK"
     }
     ```

   - **API Documentation:**
     
     Visit [http://localhost:8080/docs](http://localhost:8080/docs) to access the Swagger UI and interact with your API endpoints.

4. **Monitor Logs:**

   Check the container logs for any runtime errors or issues:

   ```bash
   docker logs -f <container_id>
   ```

   Replace `<container_id>` with your actual container ID or name.

---

## 📤 **Deployment to Google Cloud Run**

1. **Build and Push Docker Image to Google Container Registry (GCR) or Artifact Registry:**

   ```bash
   docker build -t gcr.io/your-gcp-project-id/gcp-fastapi-api:latest .
   docker push gcr.io/your-gcp-project-id/gcp-fastapi-api:latest
   ```

2. **Deploy to Cloud Run:**

   ```bash
   gcloud run deploy gcp-fastapi-api \
     --image gcr.io/your-gcp-project-id/gcp-fastapi-api:latest \
     --platform managed \
     --region your-region \
     --allow-unauthenticated \
     --set-env-vars FIRESTORE_COLLECTION="your-collection",BUCKET_NAME="your-bucket",PUBSUB_TOPIC="projects/project-id/topics/your-topic",GOOGLE_APPLICATION_CREDENTIALS="/app/creds/service-account.json" \
     --add-cloudsql-instances your-cloudsql-instance
   ```

   **Notes:**

   - **`--allow-unauthenticated`:** Adjust based on your authentication requirements.
   - **Environment Variables:** Ensure all required variables are set.
   - **Service Account Credentials:** Provide access to the service account by securely managing credentials.

3. **Verify Deployment:**

   - **Health Check:**
     
     ```bash
     curl https://your-cloud-run-service-url/health
     ```

     **Expected Response:**

     ```json
     {
       "status": "OK"
     }
     ```

   - **API Documentation:**
     
     Visit `https://your-cloud-run-service-url/docs` in your browser to access the Swagger UI.

---

## 🧪 **Testing**

1. **Unit Tests:**

   Implement unit tests for your Pydantic models, services, and routers to ensure functionality.

   **Example:**

   ```python
   # tests/test_models.py

   from app.models.item import Item, Status, OutputFiles
   from datetime import datetime

   def test_item_model():
       data = {
           "file_name": "data.csv",
           "uploaded_by_user_id": "user123",
           "phone_columns": ["phone1", "phone2"],
           "column_aliases": {"phone1": "Phone Number 1", "phone2": "Phone Number 2"},
           "phone_column_indexes": [0, 1],
           "phone_order_indexes": [1, 0],
           "has_header_row": True,
           "timestamp": datetime.utcnow(),
           "status": {
               "stage": "uploaded",
               "last_updated": datetime.utcnow()
           },
           "output_files": {
               "clean_file_path": "clean_data.csv",
               "invalid_file_path": "invalid_data.csv",
               "dnc_file_path": "dnc_data.csv"
           }
       }

       item = Item(**data)
       assert item.file_name == "data.csv"
       assert item.status.stage == "uploaded"
       assert item.output_files.clean_file_path == "clean_data.csv"
   ```

2. **Integration Tests:**

   Test the interaction between different components (e.g., Firestore and the API endpoints).

3. **Manual Testing:**

   Use tools like **Postman** or **cURL** to manually test API endpoints.

   **Example Using cURL:**

   ```bash
   curl -H "Authorization: Bearer <YOUR_GOOGLE_ID_TOKEN>" \
        -H "Content-Type: application/json" \
        -d '{"file_name": "data.csv", "uploaded_by_user_id": "user123", ...}' \
        http://localhost:8080/firestore/create
   ```

---

## 📖 **Documentation**

### **API Endpoints:**

- **Health Check:**

  ```http
  GET /health
  ```

  **Response:**

  ```json
  {
    "status": "OK"
  }
  ```

- **Firestore Operations:**
  
  - **Create Document:** `POST /firestore/create`
  - **Get Document:** `GET /firestore/{doc_id}`
  - **Update Document:** `PUT /firestore/{doc_id}`
  - **Delete Document:** `DELETE /firestore/{doc_id}`

- **Cloud Storage Operations:**
  
  - **Upload File:** `POST /storage/upload`
  - **Download File:** `GET /storage/download/{file_name}`

- **Pub/Sub Operations:**
  
  - **Publish Message:** `POST /pubsub/publish`

### **Pydantic Models:**

- **Item Model:**

  ```python
  from pydantic import BaseModel
  from typing import List, Dict, Optional
  from datetime import datetime

  class Status(BaseModel):
      stage: str
      last_updated: datetime

  class OutputFiles(BaseModel):
      clean_file_path: Optional[str] = None
      invalid_file_path: Optional[str] = None
      dnc_file_path: Optional[str] = None

  class Item(BaseModel):
      file_name: str
      uploaded_by_user_id: str
      phone_columns: List[str]
      column_aliases: Dict[str, str]
      phone_column_indexes: List[int]
      phone_order_indexes: List[int]
      has_header_row: bool
      timestamp: datetime
      status: Status
      output_files: Optional[OutputFiles] = None
  ```

---

## 🐞 **Troubleshooting**

1. **Permission Issues with Uvicorn:**

   **Error:**

   ```
   /usr/local/bin/python3.12: can't open file '/root/.local/bin/uvicorn': [Errno 13] Permission denied
   ```

   **Solution:**

   - Ensure `uvicorn` is installed globally without the `--user` flag.
   - Verify that the Docker container runs as a non-root user with appropriate permissions.
   - Use the updated `Dockerfile` provided above to resolve permission issues.

2. **Authentication Errors:**

   - **Ensure:** Google OAuth Client ID is correctly set in environment variables.
   - **Check:** Service account has the necessary permissions.
   - **Verify:** Tokens are correctly obtained and included in requests.

3. **Firestore Connection Issues:**

   - **Verify:** `GOOGLE_APPLICATION_CREDENTIALS` points to a valid service account JSON.
   - **Check:** Firestore is enabled in your GCP project.

4. **Cloud Storage Errors:**

   - **Ensure:** GCS bucket name is correctly specified and the service account has access.
   - **Check:** Proper permissions are set for uploading and downloading files.

5. **Pub/Sub Failures:**

   - **Verify:** Pub/Sub topic exists and is correctly specified in environment variables.
   - **Check:** Service account has Pub/Sub Publisher role.

---

## 🤝 **Contributing**

Contributions are welcome! Please follow these steps:

1. **Fork the Repository.**
2. **Create a Feature Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes:**

   Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) guidelines.

4. **Push to the Branch:**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request.**

---

## 📜 **License**

[MIT](LICENSE)

---

## 📫 **Contact**

For any inquiries or support, please contact [kelvinrojas66@gmail.com](mailto:kelvinrojas66@gmail.com).

---

## 🔗 **References**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Cloud Firestore](https://cloud.google.com/firestore)
- [Google Cloud Pub/Sub](https://cloud.google.com/pubsub)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Docker Documentation](https://docs.docker.com/)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

---