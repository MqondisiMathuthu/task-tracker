import os
from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return jsonify({"message": "Task Tracker is alive!"})

@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "ok", "redis": "connected"})
    except redis.exceptions.ConnectionError:
        return jsonify({"status": "degraded", "redis": "unreachable"}), 500

@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = r.lrange("tasks", 0, -1)
    return jsonify({"tasks": tasks})

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Provide JSON like {\"task\": \"buy milk\"}"}), 400
    r.rpush("tasks", task)
    return jsonify({"added": task}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
