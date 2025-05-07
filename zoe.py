# --- zoe.py ---
import streamlit as st
import time
from dotenv import load_dotenv
from app.chatbot_core import generate_response, show_final_ace_result
from app.utils import log_ace_result, log_chat, reset_chat_state
from ui.ace_handler import handle_ace_questionnaire
from ui.ui_components import (
    render_logo_header,
    render_fixed_input_style,
    render_footer,
    render_globe_button,
    render_chat_message,
    render_styled_chat,
    render_profile_sidebar
)

# --- Config ---
st.set_page_config(layout="wide", page_title="ThinkxLife", page_icon="💡")
load_dotenv()
render_logo_header()

# --- Init State ---
if "state" not in st.session_state:
    st.session_state.state = reset_chat_state()
state = st.session_state.state

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Name & Age Collection ---
if not state["name"]:
    st.subheader("🧍 Let's get to know you")
    state["name"] = st.text_input("What is your name?", placeholder="Enter your First Name")

if state["age"] is None:
    age_input = st.text_input("What is your age?", placeholder="Enter your age")
    if age_input.strip().isdigit():
        state["age"] = int(age_input.strip())
        st.rerun()
    else:
        st.stop()

# --- Age Restriction ---
if state["age"] < 18:
    st.error("⚠️ You must be 18 years or older to use this assistant.")
    st.warning("Session ended due to age restrictions.")
    st.stop()

# --- ACE Questionnaire ---
if not state["ace_completed"]:
    if not handle_ace_questionnaire(state):
        st.stop()

# --- Post-ACE Welcome ---
if state["ace_completed"] and not st.session_state.get("show_chat_button"):
    if not st.session_state.get("ace_logged"):
        log_ace_result(state)
        st.session_state.ace_logged = True

    st.subheader("💬 ACE Questionnaire Complete")
    show_final_ace_result(state)

    ace_score = state["ace_score"]
    if ace_score <= 3:
        init_message = "🌞 Hey sunshine! What can  explore together today?"
    elif 4 <= ace_score <= 6:
        init_message = "🌻 Hello strong spirit. What woul you like to talk about today?"
    else:
        init_message = "🌸 Hello brave soul. I' here for you — what's on your mind today?"

    if st.button("Start Chat"):
        st.session_state.show_chat_button = True
        with st.spinner("Starting your chat..."):
            time.sleep(0.3)
        st.session_state.messages.append({"role": "assistant", "content": init_message})
        st.rerun()

    st.stop()

# --- Floating Globe Button ---
render_globe_button()

# --- Chat Display ---
render_styled_chat()

# --- Input Styling ---
render_fixed_input_style()

# --- Chat Interaction ---
prompt = st.chat_input("How can I help?")
if prompt:
    log_chat("user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="assets/user.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="assets/zoe.png"):
        msg_placeholder = st.empty()
        response = generate_response(prompt, st.session_state.messages)
        msg_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    log_chat("assistant", response)

# --- Sidebar ---
with st.sidebar:
    render_profile_sidebar()

# --- Footer ---
if st.session_state.get("show_chat_button"):
    render_footer()
