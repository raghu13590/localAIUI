FROM python:3.9-slim
WORKDIR /app

# Add build essentials for potential dependency compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY qwen_searxng_langchain.py .
EXPOSE 8081

# Add healthcheck for container monitoring
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8081/ || exit 1

CMD ["python", "qwen_searxng_langchain.py"]