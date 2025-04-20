import streamlit as st
from app.chatbot_core import process_ace_response

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


def handle_ace_questionnaire(state):
    if state["ace_index"] < len(ace_questions):
        st.subheader("🧍 Let's get to know you")
        q = ace_questions[state["ace_index"]]
        st.write(f"**Q{state['ace_index']+1}.** {q}")
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
    return state["ace_completed"]
