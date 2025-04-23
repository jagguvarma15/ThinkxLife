import streamlit as st


# Sidebar history showing user prompts only, clickable to scroll
def render_history():
    state = st.session_state.state

    # Stylish Name & Age Card
    st.markdown(f"""
    <div style="background-color: #ffffff;
                border-left: 6px solid #4A90E2;
                border-radius: 8px;
                padding: 15px 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <div style="font-size: 1.1rem; font-weight: bold; color: #333;">Name</div>
        <div style="font-size: 1.25rem; color: #111; margin-bottom: 10px;">{state['name']}</div>
        <div style="font-size: 1.1rem; font-weight: bold; color: #333;">Age</div>
        <div style="font-size: 1.25rem; color: #111;">{state['age']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💬 Your Prompts")

    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            label = msg["content"][:40] + ("..." if len(msg["content"]) > 40 else "")
            if st.button(f"🗨️ {label}", key=f"nav-{idx}"):
                st.session_state.scroll_to_index = idx
                st.rerun()


# Logo header
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

# Footer
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

# Input bar CSS
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