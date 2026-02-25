# BASE IMAGE
FROM python:3.10-slim


# ENV SETTINGS
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1


# SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*


# WORKDIR
WORKDIR /app


# INSTALL PYTHON DEPENDENCIES
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# COPY PROJECT FILES
COPY app ./app

# persistent storage
RUN mkdir -p /app/app/data


# PORT
EXPOSE 8000

# START SERVER
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]