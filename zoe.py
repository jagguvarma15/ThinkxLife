# --- zoe.py ---
import streamlit as st
import time
from dotenv import load_dotenv
from app.chatbot_core import generate_response, show_final_ace_result
from app.utils import log_ace_result, log_chat, reset_chat_state
from ui.ace_handler import handle_ace_questionnaire
from ui.ui_components import render_logo_header, render_fixed_input_style, render_footer, render_globe_button
from ui.advanced_ui import render_chat_message, start_chat_container, end_chat_container, render_styled_chat

load_dotenv()

st.set_page_config(layout="wide", page_title="ThinkxLife", page_icon="\U0001F4A1")  
render_logo_header()

# --- Init State ---
if "state" not in st.session_state:
    st.session_state.state = reset_chat_state()

state = st.session_state.state

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Name & Age Collection ---
if not state["name"]:
    st.subheader(f"\U0001F9CD Let's get to know you")  # 🧍
    state["name"] = st.text_input("What is your name?", placeholder="Enter your First Name")

if state["age"] is None:
    age_input = st.text_input("What is your age?", value="", placeholder="Enter your age")
    if age_input.strip().isdigit():
        state["age"] = int(age_input.strip())
        st.rerun()
    else:
        st.stop()

# Age Restriction Check
if state["age"] < 18:
    st.error("\u26A0\uFE0F You must be 18 years or older to use this assistant.")  
    st.warning("Session ended due to age restrictions for usage.")
    st.stop()

# --- ACE Questionnaire Flow ---
if not state["ace_completed"]:
    if handle_ace_questionnaire(state):
        pass  # ACE complete, move forward
    else:
        st.stop()


# --- ACE Completed: Show Thank You and Start Chat ---
if state["ace_completed"] and not st.session_state.get("show_chat_button"):
    if not st.session_state.get("ace_logged"):
        log_ace_result(state)
        st.session_state.ace_logged = True

    st.subheader("\U0001F4AD ACE Questionnaire Complete") 
    show_final_ace_result(state)

    # Personalized Initial Message Based on ACE Score
    ace_score = state["ace_score"]
    if ace_score <= 3:
        init_message = "\U0001F31E Hey sunshine! What can we explore together today?"  # 🌞
    elif 4 <= ace_score <= 6:
        init_message = "\U0001F33B Hello strong spirit. What would you like to talk about today?"  # 🌻
    else:
        init_message = "\U0001F338 Hello brave soul. I'm here for you — what’s on your mind today?"  # 🌸

    # Only ADD the message if Start Chat is clicked
    if st.button("Start Chat"):
        st.session_state.show_chat_button = True
        with st.spinner("Starting your chat..."):
            time.sleep(0.3)
        # Add initial message to messages only AFTER clicking Start Chat
        st.session_state.messages.append({"role": "assistant", "content": init_message})
        st.rerun()

    st.stop()

render_globe_button()

# --- Sidebar ---
with st.sidebar:
    from ui.ui_components import render_history
    render_history()

# --- Styled Chat Messages ---
render_styled_chat()

# --- Fixed Prompt Input Bar ---
render_fixed_input_style()

# --- Chat Logic ---
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

# --- Footer (only after Start Chat) ---
if st.session_state.get("show_chat_button"):
    render_footer()
