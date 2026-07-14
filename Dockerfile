FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY programa/ .

RUN mkdir -p data

CMD ["python", "main.py"]