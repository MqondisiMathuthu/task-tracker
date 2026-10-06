from flask import Flask, jsonify

app = Flask(__name__)

tasks = []

@app.route("/")
def home():
    return jsonify({"message": "Task Tracker is alive!"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
