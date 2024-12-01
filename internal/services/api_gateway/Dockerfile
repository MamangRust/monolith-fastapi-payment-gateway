FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dari services/api_gateway
COPY services/api_gateway/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy lib ke dalam container
COPY lib /app/lib

# Copy seluruh api_gateway service
COPY services/api_gateway /app

# Tambahkan PYTHONPATH
ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8080

WORKDIR /app
CMD ["python", "main.py"]
