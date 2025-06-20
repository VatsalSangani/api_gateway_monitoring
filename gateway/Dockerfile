# gateway/Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔧 Install Docker CLI inside the container
RUN apt update && apt install -y docker.io

# Copy the gateway app files
COPY . .

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]