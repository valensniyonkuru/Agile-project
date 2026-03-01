"""
Task API - Sprint 1 & 2 increments.
Endpoints: create, list, get by ID, update, delete; health and logging.
"""
import logging
import uuid
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
tasks_store = {}


def _task_json(tid, title, description, status="open"):
    return {"id": tid, "title": title, "description": description, "status": status}


@app.route("/health", methods=["GET"])
def health():
    """Health endpoint for monitoring (Sprint 2)."""
    logger.info("Health check requested")
    return jsonify({"status": "ok"}), 200


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """List all tasks (US-2)."""
    logger.info("Listing all tasks")
    out = [{"id": k, **v} for k, v in tasks_store.items()]
    return jsonify(out), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a task (US-1)."""
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    tid = str(uuid.uuid4())
    tasks_store[tid] = {"title": title, "description": description, "status": "open"}
    logger.info("Task created: %s", tid)
    return jsonify(_task_json(tid, title, description)), 201


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    """Get a single task by ID (US-3)."""
    if task_id not in tasks_store:
        logger.warning("Task not found: %s", task_id)
        return jsonify({"error": "task not found"}), 404
    t = tasks_store[task_id]
    return jsonify(_task_json(task_id, t["title"], t["description"], t["status"])), 200


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Update a task (US-4)."""
    if task_id not in tasks_store:
        logger.warning("Task not found for update: %s", task_id)
        return jsonify({"error": "task not found"}), 404
    data = request.get_json() or {}
    t = tasks_store[task_id]
    if "title" in data and data["title"] is not None:
        t["title"] = str(data["title"]).strip() or t["title"]
    if "description" in data:
        t["description"] = str(data["description"])
    if "status" in data and data["status"] in ("open", "done"):
        t["status"] = data["status"]
    logger.info("Task updated: %s", task_id)
    return jsonify(_task_json(task_id, t["title"], t["description"], t["status"])), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task (US-5)."""
    if task_id not in tasks_store:
        logger.warning("Task not found for delete: %s", task_id)
        return jsonify({"error": "task not found"}), 404
    del tasks_store[task_id]
    logger.info("Task deleted: %s", task_id)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
