FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY qwen_searxng_langchain.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "qwen_searxng_langchain.py"]
