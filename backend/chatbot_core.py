from openai import OpenAI
from dotenv import load_dotenv
import os

from embed_utils import search_faiss_index

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
