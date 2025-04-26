import streamlit as st
import json
from app.chatbot_core import compute_ace_score, process_ace_response

with open("data/ace_questions.json", "r") as f:
    ace_questions = json.load(f)


def handle_ace_questionnaire(state):
    if state["ace_index"] < len(ace_questions):
        st.subheader("\U0001F9CD Let's get to know you")
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

    # When questionnaire is done:
    if state["ace_index"] >= len(ace_questions) and not state["ace_completed"]:
        state["ace_completed"] = True
        state["ace_score"] = compute_ace_score(state["ace_responses"])
        return True

    return False
