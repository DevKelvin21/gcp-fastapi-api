# Use a lightweight base image
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set the entrypoint to run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
