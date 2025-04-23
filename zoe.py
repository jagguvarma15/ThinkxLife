#--- zoe.py ---
import streamlit as st
import time
from dotenv import load_dotenv
from app.chatbot_core import reset_chat_state, generate_response
from app.utils import log_ace_result, log_chat
from ui.ace_handler import handle_ace_questionnaire
from ui.ui_components import render_logo_header, render_fixed_input_style, render_footer
from ui.advanced_ui import render_chat_message, start_chat_container, end_chat_container

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
if not state["name"]:
    st.subheader(f"{chr(0x1F9CD)} Let's get to know you")
    state["name"] = st.text_input("What is your name?", placeholder="Enter your First Name")
    #st.stop()

if state["age"] is None:
    age_input = st.text_input("What is your age?", value="", placeholder="Enter your age")
    if age_input.strip().isdigit():
        state["age"] = int(age_input.strip())
        st.rerun()
    else:
        st.stop()


# Age Restriction Check (only after both fields filled)
if state["age"] < 18:
    st.error("⚠️ You must be 18 years or older to use this assistant.")
    st.warning("Session ended due to age restrictions for usage.")
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
    from ui.ui_components import render_history
    render_history()


# --- Styled Chat Messages ---
start_chat_container()
for idx, message in enumerate(st.session_state.messages):
    anchor_id = f"msg-{idx}"
    if idx == st.session_state.get("scroll_to_index"):
        st.markdown(f"<div id='{anchor_id}'></div>", unsafe_allow_html=True)
        st.components.v1.html(f"<script>document.getElementById('{anchor_id}').scrollIntoView({{ behavior: 'smooth' }});</script>", height=0)
    render_chat_message(message["role"], message["content"])
end_chat_container()

# --- Fixed Prompt Input Bar ---
render_fixed_input_style()

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

# --- Footer (visible only in chat mode) ---
if st.session_state.get("show_chat_button"):
    render_footer()
