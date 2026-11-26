FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# Etape de test : si un test echoue, Jenkins s'arrete ici
FROM base AS test
COPY test_app.py .
RUN python -m unittest -v

FROM base AS final
USER nobody
EXPOSE 8000
# Un seul worker : les compteurs Prometheus restent coherents
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "--no-control-socket", "app:app"]
