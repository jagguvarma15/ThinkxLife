from openai import OpenAI
from dotenv import load_dotenv
from app.utils import compute_ace_score
import streamlit as st
from app.config import OPENAI_API_KEY
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever()

def generate_response(prompt, message_history):
    docs = retriever.get_relevant_documents(prompt)
    context_chunks = [doc.page_content for doc in docs]

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

import streamlit as st

def process_ace_response(state, response):
    """
    Process the user's ACE questionnaire response and update the state.
    """
    if "ace_responses" not in state:
        state["ace_responses"] = []

    if response == "Yes":
        state["ace_responses"].append(1.0)    # Full 1 point for Yes
    elif response == "No":
        state["ace_responses"].append(0.0)    # 0 point for No
    elif response == "Skip":
        state["ace_responses"].append(0.25)   # 0.25 partial point for Skip

    state["ace_index"] += 1

def compute_ace_score(responses):
    """
    Compute the final ACE score from the user's responses.
    """
    return round(sum(responses), 2)  # Sum all points and round to 2 decimal places

def show_final_ace_result(state):
    """
    Display the user's ACE score and an empathetic, color-coded message based on score.
    """
    score = compute_ace_score(state["ace_responses"])

    st.success(f"Thank you {state['name']}. Your ACE Score is **{score}/10**.")

    if score <= 3:
        st.info(
            "\U0001F49A Your early experiences suggest fewer major stressors. "
            "That's wonderful, but remember — everyone's journey is important. "
            "I'm here to support your growth and dreams! \U0001F31F"
        )
    elif 4 <= score <= 6:
        st.warning(
            "\U0001F49B You may have faced some tough experiences growing up. "
            "Your resilience shines through. "
            "I'm here to talk, listen, and walk with you whenever you need. \U0001F91D"
        )
    elif score >= 7:
        st.error(
            "\U0001F49C You’ve carried a lot — more than anyone should have to. "
            "Please know: your story matters, your feelings are valid, "
            "and you deserve kindness and healing. "
            "I'm here for you. \U0001F49C"
        )

    if any(r == 0.25 for r in state["ace_responses"]):
        st.caption(
            "\U0001F4DD (We noticed you skipped a few questions — that's perfectly okay. "
            "Your comfort and safety come first!)"
        )
