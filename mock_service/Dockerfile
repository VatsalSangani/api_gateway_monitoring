# mock_service/Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the mock service app files
COPY . .

# Run the mock backend with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
