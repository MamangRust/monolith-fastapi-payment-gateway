FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY services/topup_service/requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service source code
COPY services/topup_service/ .

# Copy the shared libraries
COPY libs/ /app/libs

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8003


# Command to run the application
CMD ["python", "main.py"]
