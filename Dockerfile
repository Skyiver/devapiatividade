FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN find . -name "*.py" -print

ENV PYTHONPATH=/app

EXPOSE 5001

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5001", "atividade_service.app:app"]