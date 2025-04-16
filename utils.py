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
