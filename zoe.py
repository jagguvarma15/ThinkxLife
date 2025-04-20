#--- zoe.py ---
import streamlit as st
import time
from dotenv import load_dotenv
from app.chatbot_core import reset_chat_state, generate_response
from app.utils import log_ace_result, log_chat
from ui.ace_handler import handle_ace_questionnaire
from ui.ui_components import render_user_info, render_logo_header, render_fixed_input_style, render_celebration_animation, render_footer
from ui.advanced_ui import inject_chat_styles, render_chat_message, start_chat_container, end_chat_container

load_dotenv()

st.set_page_config(layout="wide", page_title="ThinkxLife", page_icon="💡")
render_logo_header()

# --- Init State ---
if "state" not in st.session_state:
    st.session_state.state = reset_chat_state()

state = st.session_state.state

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! How can I support you today?"}]

# --- Name & Age Collection ---
if not state["name"] or not state["age"]:
    st.subheader(f"{chr(0x1F9CD)} Let's get to know you")
    state["name"] = st.text_input("What is your name?")
    state["age"] = st.number_input("What is your age?", min_value=5, max_value=100)
    st.stop()

# --- ACE Questionnaire Flow ---
if not state["ace_completed"]:
    handle_ace_questionnaire(state)
    st.stop()

# --- ACE Completed: Show Thank You and Start Chat ---
if state["ace_completed"] and not st.session_state.get("show_chat_button"):
    if not st.session_state.get("ace_logged"):
        log_ace_result(state)
        st.session_state.ace_logged = True

    st.subheader("💭 ACE Questionnaire Complete")
    st.success(f"Thank you {state['name']} 🙏. Your ACE Score is **{state['ace_score']}/10**.")
    st.info("This doesn't define you — it's just one way to understand early experiences. I'm here to talk whenever you're ready 💜.")

    #render_celebration_animation()

    if st.button("Start Chat"):
        st.session_state.show_chat_button = True
        with st.spinner("Starting your chat..."):
            time.sleep(0.3)
        st.rerun()

    st.stop()

# --- Sidebar  ---
with st.sidebar:
    st.title("🧠 Chat History")
    # You can optionally add session-based chat tabs here

# --- Chat Header ---
render_user_info()

# --- Styled Chat Messages ---
inject_chat_styles()
start_chat_container()
for message in st.session_state.messages:
    render_chat_message(message["role"], message["content"])
end_chat_container()

# --- Fixed Prompt Input Bar ---
render_fixed_input_style()

prompt = st.chat_input("How can I help?")
if prompt:
    log_chat("user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        response = generate_response(prompt, st.session_state.messages)
        msg_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    log_chat("assistant", response)

# --- Footer (visible only in chat mode) ---
if st.session_state.get("show_chat_button"):
    render_footer()
