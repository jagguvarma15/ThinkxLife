# advanced_ui.py
import streamlit as st
import os

AVATAR_USER = "assets/zoe.png"
AVATAR_BOT = "assets/user.png"

# Inject custom chat styles
def inject_chat_styles():
    with open("ui/chat_styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render a single chat message
def render_chat_message(role, content):
    bubble_class = "bot" if role == "assistant" else "user"
    avatar_path = AVATAR_BOT if role == "assistant" else AVATAR_USER
    wrapper_class = f"message-wrapper {bubble_class}"

    with st.container():
        st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
        cols = st.columns([1, 12]) if role == "assistant" else st.columns([12, 1])

        with cols[0 if role == "assistant" else 1]:
            st.image(avatar_path, width=32)

        with cols[1 if role == "assistant" else 0]:
            st.markdown(f"<div class='chat-bubble {bubble_class}'>{content}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# Optional: Wrap the whole chat area
def start_chat_container():
    st.markdown('<div class="custom-chat-container">', unsafe_allow_html=True)

def end_chat_container():
    st.markdown('</div>', unsafe_allow_html=True)
