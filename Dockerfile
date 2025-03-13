# Use a lightweight Python base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files after installing dependencies
COPY . /app
COPY .* /app/
# Expose gRPC server port
EXPOSE 50051

# Run the gRPC server
CMD ls -l /app && ls -l && pwd && python /app/grpc_server1.py
