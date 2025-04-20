import streamlit as st
from streamlit_lottie import st_lottie
import requests


def render_user_info():
    """Top bar showing name and age"""
    state = st.session_state.state
    if state["name"] and state["age"]:
        st.markdown(f"""
            <div style="background-color:#f0f2f6;
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:10px;
                        text-align:center;">
                <strong>User:</strong> {state['name']} &nbsp;&nbsp;
                <strong>Age:</strong> {state['age']}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("User info will appear here after name and age are entered.")

def render_history():
    """Sidebar history tab on the right"""
    if "messages" in st.session_state:
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"**Zoe:** {msg['content']}")
    else:
        st.write("No messages yet.")

def render_logo_header():
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/jagguvarma15/ThinkxLife/main/assets/logo.png' width='60' style='vertical-align: middle; margin-right: 10px;' />
            <span style='font-size: 2em; font-weight: bold; vertical-align: middle;'>Think Round, Inc.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_fixed_input_style():
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

    
def render_celebration_animation():
    url = "https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json"
    res = requests.get(url)
    if res.status_code == 200:
        st_lottie(res.json(), height=200, speed=1, loop=False)

def render_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 5px;
            right: 10px;
            font-size: 0.8rem;
            color: #999999;
        }
        </style>
        <div class="footer">
            © 2025 Think Round, Inc.
        </div>
        """,
        unsafe_allow_html=True
    )
