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
COPY services/email_service/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy lib ke dalam container
COPY lib /app/lib

# Copy seluruh email_service service
COPY services/email_service /app

# Ensure wait-for-it.sh is executable
RUN chmod +x /app/wait-for-it.sh

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8008

# Command to run the application
ENTRYPOINT ["bash", "/app/wait-for-it.sh", "kafka:9092", "--"]

CMD ["python", "main.py"]
