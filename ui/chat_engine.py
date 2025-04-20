import streamlit as st
from app.chatbot_core import generate_response

USER_AVATAR = "🕤"
BOT_AVATAR = "🤖"

def run_chatbot(state):
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
            response = generate_response(prompt, st.session_state.messages)
            message_placeholder.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})