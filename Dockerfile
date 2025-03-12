# Use a lightweight Python base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install FastAPI and Uvicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Expose gRPC server port
EXPOSE 50051

# Run the gRPC server
CMD ["python", "grpc_server.py"]
