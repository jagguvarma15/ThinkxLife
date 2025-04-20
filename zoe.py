import streamlit as st
from dotenv import load_dotenv
from app.chatbot_core import reset_chat_state, generate_response
from ui.ace_handler import handle_ace_questionnaire
from ui.ui_components import render_user_info, render_history

load_dotenv()

st.set_page_config(layout="wide", page_title="ThinkxLife", page_icon="💡")
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/jagguvarma15/ThinkxLife/main/assets/logo.png' width='60' style='vertical-align: middle; margin-right: 10px;' />
        <span style='font-size: 2em; font-weight: bold; vertical-align: middle;'>Think Round, Inc.</span>
    </div>
    """,
    unsafe_allow_html=True
)

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
just_finished = handle_ace_questionnaire(state)

if just_finished and not st.session_state.get("show_chat_button"):
    st.subheader("💭 ACE Questionnaire Complete")
    st.success(f"Thank you {state['name']} 🙏. Your ACE Score is **{state['ace_score']}/10**.")
    st.info("This doesn't define you — it's just one way to understand early experiences. I'm here to talk whenever you're ready 💜.")
    if st.button("Start Chatting"):
        st.session_state.show_chat_button = True
        st.rerun()
    st.stop()

# --- Sidebar like ChatGPT ---
with st.sidebar:
    st.title("🧠 Chat History")
    render_history()

# --- Chat Header ---
render_user_info()

# --- Chat Messages ---
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Fixed Prompt Input Bar ---
st.markdown(
    """
    <style>
        .stChatInputContainer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem 2rem;
            background: white;
            z-index: 9999;
            box-shadow: 0 -1px 10px rgba(0,0,0,0.1);
        }
        .block-container {
            padding-bottom: 100px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

prompt = st.chat_input("How can I help?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        response = generate_response(prompt, st.session_state.messages)
        msg_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
