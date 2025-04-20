import streamlit as st
from ace_questions import ace_questions
from utils import compute_ace_score

def handle_ace_questionnaire(state):
    st.subheader("💭 ACE Questionnaire")
    if state["ace_index"] < len(ace_questions):
        q = ace_questions[state["ace_index"]]
        st.write(f"**Q{state['ace_index']+1}.** {q}")
        col1, col2, col3 = st.columns(3)
        if col1.button("Yes"):
            state["ace_responses"].append("Yes")
            state["ace_index"] += 1
        if col2.button("No"):
            state["ace_responses"].append("No")
            state["ace_index"] += 1
        if col3.button("Skip"):
            state["ace_responses"].append("Skip")
            state["ace_index"] += 1
        st.stop()
    else:
        score = compute_ace_score(state["ace_responses"])
        st.success(f"Thank you {state['name']} 🙏. Your ACE Score is **{score}/10**.")
        st.info("This doesn't define you — it's just one way to understand early experiences. I'm here to talk whenever you're ready 💜.")
        state["ace_completed"] = True
