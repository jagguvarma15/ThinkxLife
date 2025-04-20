import streamlit as st
from dotenv import load_dotenv
from app.zoe import reset_chat_state, process_ace_response, generate_response
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

# --- Name & Age Collection ---
if not state["name"] or not state["age"]:
    st.subheader(f"{chr(0x1F9CD)} Let's get to know you")
    state["name"] = st.text_input("What is your name?")
    state["age"] = st.number_input("What is your age?", min_value=5, max_value=100)
    st.stop()

# --- ACE Questions Inline (avoiding import issues) ---
ace_questions = [
    "Did a parent or adult in the household often swear at you, insult you, or humiliate you?",
    "Did a parent or adult in the household often push, grab, slap, or throw something at you?",
    "Did an adult ever touch or fondle you in a sexual way?",
    "Did you often feel that no one in your family loved you or thought you were important?",
    "Did you often feel that you didn't have enough to eat, had to wear dirty clothes, or had no one to protect you?",
    "Was a biological parent ever lost to you through divorce, abandonment, or other reason?",
    "Was your mother or stepmother often pushed, grabbed, slapped, or had something thrown at her?",
    "Did you live with anyone who was a problem drinker or used street drugs?",
    "Was a household member depressed, mentally ill, or did a household member attempt suicide?",
    "Did a household member go to prison?",
]

# --- ACE Questionnaire Flow ---
if not state["ace_completed"]:
    st.subheader("💭 ACE Questionnaire (Adverse Childhood Experiences)")
    if state["ace_index"] < len(ace_questions):
        question = ace_questions[state["ace_index"]]
        st.write(f"**Q{state['ace_index'] + 1}.** {question}")
        col1, col2, col3 = st.columns(3)
        if col1.button("Yes"):
            process_ace_response(state, "Yes")
            st.rerun()
        if col2.button("No"):
            process_ace_response(state, "No")
            st.rerun()
        if col3.button("Skip"):
            process_ace_response(state, "Skip")
            st.rerun()
        st.stop()
    else:
        st.success(f"Thanks {state['name']}! Your ACE Score is {state['ace_score']}/10")
        st.info("This doesn't define you — it's just a reference. Zoe is here to help 💜")

# --- Chat State Init ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! How can I support you today?"}]

# --- Layout ---
render_user_info()
col_main, col_side = st.columns([3, 1])

# --- Chat Interface ---
with col_main:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            msg_placeholder = st.empty()
            response = generate_response(prompt, st.session_state.messages)
            msg_placeholder.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# --- Chat History Sidebar ---
with col_side:
    render_history()
