FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/api_gateway/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy lib ke dalam container
COPY lib /app/lib

# Copy seluruh api_gateway service
COPY services/api_gateway /app

COPY alembic.ini /app

# Tambahkan PYTHONPATH untuk memastikan aplikasi dapat menemukan modul dengan benar
ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Jalankan Alembic migrasi saat build
# RUN alembic upgrade head || echo "Alembic migration failed during build, check logs."

EXPOSE 8080

WORKDIR /app
ENTRYPOINT ["bash", "/app/wait-for-it.sh", "postgres:5432", "--"]
CMD ["sh", "-c", "alembic upgrade head && python main.py"]

