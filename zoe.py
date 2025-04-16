from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from embed_utils import search_faiss_index
from ace_questions import ace_questions
from utils import compute_ace_score, reset_chat_state
import shelve
import os

load_dotenv()


st.set_page_config(page_title="ThinkxLife", page_icon="💡")

# Logo and Title in same row
col1, col2 = st.columns([1, 6])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.markdown("<h1 style='padding-top: 15px;'>Think Round, Inc.</h1>", unsafe_allow_html=True)

st.subheader("Meet Zoe - Your Empathetic AI Assistant 💬")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

if "state" not in st.session_state:
    st.session_state.state = reset_chat_state()

state = st.session_state.state

# Name and Age
if not state["name"] or not state["age"]:
    st.subheader("🧍 Let's get to know you")
    state["name"] = st.text_input("What is your name?")
    state["age"] = st.number_input("What is your age?", min_value=5, max_value=100, step=1)
    st.stop()

# ACE Questionnaire
if not state["ace_completed"]:
    st.subheader("💭 ACE Questionnaire (Adverse Childhood Experiences)")
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
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hi there! How can I support you today?"}]



# --- Chat UI ---
if state["ace_completed"]:
    # Display chat history
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""

            # ✅ Add this line to retrieve relevant chunks
            context_chunks = search_faiss_index(prompt)
            context_prompt = "\n\n".join(context_chunks)

            system_prompt = {
                "role": "system",
                "content": f"You are Zoe, an empathetic assistant. Use the following context to help answer the user's question:\n\n{context_prompt}"
            }

            chat_history = [system_prompt] + st.session_state.messages

            for response in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history,
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown("**Zoe:** " + full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
