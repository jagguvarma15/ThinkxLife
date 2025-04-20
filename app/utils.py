import csv
import os
from datetime import datetime

def compute_ace_score(responses):
    return sum(1 for r in responses if r == "Yes")

def reset_chat_state():
    return {
        "name": "",
        "age": None,
        "ace_index": 0,
        "ace_responses": [],
        "ace_completed": False,
        "messages": []
    }


def log_ace_result(state):
    log_file = "logs/ace_logs.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    yes_questions = [i+1 for i, ans in enumerate(state["ace_responses"]) if ans == "Yes"]
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            state["name"],
            state["age"],
            state["ace_score"],
            ";".join(map(str, yes_questions))
        ])

def log_chat(role, content):
    log_file = "logs/chat_logs.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            role,
            content
        ])
