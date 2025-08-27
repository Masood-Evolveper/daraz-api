FROM python:3.13-slim

WORKDIR /app

# Install git and deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Build arg for token
ARG GITHUB_TOKEN
ARG GITHUB_USER

# Clone private repo (replace with your repo URL)
RUN git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/Masood-Evolveper/daraz-api.git .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]