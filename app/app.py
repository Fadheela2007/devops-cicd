import os
import socket
import time

from flask import Flask, Response, g, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

# Modifier ce message puis faire "git push" pour tester la chaine CI/CD
MESSAGE = "Bonjour ! Application deployee par Jenkins sur Kubernetes."

VERSION = os.getenv("APP_VERSION", "dev")

app = Flask(__name__)

REQUESTS = Counter("http_requests_total", "Nombre de requetes HTTP", ["endpoint", "status"])
DURATION = Histogram("http_request_duration_seconds", "Duree des requetes HTTP", ["endpoint"])
INFO = Gauge("app_info", "Version deployee", ["version"])
INFO.labels(version=VERSION).set(1)


@app.before_request
def start_timer():
    g.start = time.perf_counter()


@app.after_request
def record_metrics(response):
    endpoint = request.url_rule.rule if request.url_rule else "inconnu"
    if endpoint not in ("/metrics", "/health"):
        REQUESTS.labels(endpoint=endpoint, status=str(response.status_code)).inc()
        DURATION.labels(endpoint=endpoint).observe(time.perf_counter() - g.start)
    return response


@app.get("/")
def home():
    return (
        "<!doctype html><meta charset='utf-8'><title>Demo DevOps</title>"
        f"<h1>{MESSAGE}</h1>"
        f"<p>Version (numero du build Jenkins) : <b>{VERSION}</b></p>"
        f"<p>Pod Kubernetes : <b>{socket.gethostname()}</b></p>"
    )


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


@app.get("/erreur")
def error():
    # Erreur volontaire pour la voir apparaitre dans Grafana
    return {"erreur": "erreur de demonstration"}, 500


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)
