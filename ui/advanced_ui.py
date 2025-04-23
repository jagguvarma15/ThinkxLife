# advanced_ui.py
import streamlit as st
import os

AVATAR_USER = "assets/user.png"
AVATAR_BOT = "assets/zoe.png"

# Render a single chat message
def render_chat_message(role, content):
    bubble_class = "bot" if role == "assistant" else "user"
    avatar_path = AVATAR_BOT if role == "assistant" else AVATAR_USER
    wrapper_class = f"message-wrapper {bubble_class}"

    with st.container():
        st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
        cols = st.columns([1, 12]) if role == "assistant" else st.columns([12, 1])

        with cols[0 if role == "assistant" else 1]:
            try:
                st.image(avatar_path, width=32)
            except:
                st.markdown("🤖" if role == "assistant" else "🧍")

        with cols[1 if role == "assistant" else 0]:
            align_style = "text-align: right;" if role != "assistant" else ""
            st.markdown(f"<div class='chat-bubble {bubble_class}' style='{align_style}'>{content}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# Optional: Wrap the whole chat area
def start_chat_container():
    st.markdown('<div class="custom-chat-container">', unsafe_allow_html=True)

def end_chat_container():
    st.markdown('</div>', unsafe_allow_html=True)
