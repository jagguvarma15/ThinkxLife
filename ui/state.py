import streamlit as st

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_age" not in st.session_state:
        st.session_state.user_age = ""
