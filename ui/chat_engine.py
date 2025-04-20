import streamlit as st
from openai import OpenAI
from embed_utils import search_faiss_index
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_chatbot(state):
    USER_AVATAR = "👤"
    BOT_AVATAR = "🤖"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi there! How can I support you today?"}]

    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""

            context_chunks = search_faiss_index(prompt)
            context_prompt = "\n\n".join(context_chunks)

            system_prompt = {
                "role": "system",
                "content": f"You are Zoe, an empathetic assistant. Use the following context to help answer the user's question:\n\n{context_prompt}"
            }

            chat_history = [system_prompt] + st.session_state.messages

            for response in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history,
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown("**Zoe:** " + full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
