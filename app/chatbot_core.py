from openai import OpenAI
from dotenv import load_dotenv
from app.embed_utils import search_faiss_index
from app.utils import compute_ace_score, reset_chat_state
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def init_chat():
    return [{"role": "assistant", "content": "Hi there! How can I support you today?"}]

def process_ace_response(state, answer):
    state["ace_responses"].append(answer)
    state["ace_index"] += 1
    if state["ace_index"] >= 10:
        score = compute_ace_score(state["ace_responses"])
        state["ace_score"] = score
        state["ace_completed"] = True
    return state

def generate_response(prompt, message_history):
    context_chunks = search_faiss_index(prompt)
    context_prompt = "\n\n".join(context_chunks)

    system_prompt = {
        "role": "system",
        "content": f"You are Zoe, an empathetic assistant. Use the following context to help answer the user's question:\n\n{context_prompt}"
    }

    chat_history = [system_prompt] + message_history
    full_response = ""

    for response in client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        stream=True,
    ):
        full_response += response.choices[0].delta.content or ""

    return full_response
