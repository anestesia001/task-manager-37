import os
import logging

import requests
from flask import Flask, render_template
from flask import request, redirect, url_for, jsonify


app = Flask(__name__)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
).rstrip("/")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


@app.errorhandler(requests.RequestException)
def handle_backend_error(error):
    logger.error("Backend request failed: %s", error)

    return render_template(
        "index.html",
        tasks=[],
        stats={},
        error="Backend API unavailable"
    ), 503


@app.get("/")
def index():
    tasks_response = requests.get(
        f"{BACKEND_URL}/tasks",
        timeout=5
    )
    tasks_response.raise_for_status()

    stats_response = requests.get(
        f"{BACKEND_URL}/stats",
        timeout=5
    )
    stats_response.raise_for_status()

    return render_template(
        "index.html",
        tasks=tasks_response.json(),
        stats=stats_response.json(),
        error=None
    )


@app.post("/tasks")
def create_task():
    task = {
        "title": request.form["title"],
        "description": request.form.get("description", "")
    }

    response = requests.post(
        f"{BACKEND_URL}/tasks",
        json=task,
        timeout=5
    )
    response.raise_for_status()

    return redirect(url_for("index"))


@app.post("/tasks/<int:task_id>/status")
def update_task(task_id):
    response = requests.patch(
        f"{BACKEND_URL}/tasks/{task_id}",
        json={"status": request.form["status"]},
        timeout=5
    )
    response.raise_for_status()

    return redirect(url_for("index"))


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    response = requests.delete(
        f"{BACKEND_URL}/tasks/{task_id}",
        timeout=5
    )
    response.raise_for_status()

    return redirect(url_for("index"))


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        service="frontend"
    )


@app.get("/ready")
def readiness():
    try:
        response = requests.get(
            f"{BACKEND_URL}/ready",
            timeout=5
        )
        response.raise_for_status()

        return jsonify(
            status="ready",
            backend="connected"
        )

    except requests.RequestException:
        return jsonify(
            status="not_ready",
            backend="unavailable"
        ), 503