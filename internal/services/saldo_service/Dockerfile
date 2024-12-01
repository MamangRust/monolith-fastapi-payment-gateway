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
COPY services/saldo_service/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy lib ke dalam container
COPY lib /app/lib

# Copy seluruh api_gateway service
COPY services/saldo_service /app


# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


EXPOSE 8002

# Command to run the application
CMD ["python", "main.py"]
