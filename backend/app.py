from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
import datetime

from chatbot_core import generate_response  

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Log chat messages to CSV (optional)
CHAT_LOG_FILE = "logs/chat_logs.csv"
os.makedirs("logs", exist_ok=True)

def log_message(user_msg, bot_msg):
    with open(CHAT_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), user_msg, bot_msg])

# Log user info to a separate CSV
USER_LOG_FILE = "logs/user_logs.csv"

@app.route("/user", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    if not name or not age:
        return jsonify({"error": "Name and age required"}), 400

    with open(USER_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), name, age])

    return jsonify({"message": "User registered successfully"}), 200


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    # Get response from Zoe (OpenAI + FAISS logic)
    try:
        bot_response = generate_response(user_message)
        log_message(user_message, bot_response)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
