import streamlit as st

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
    st.subheader("🕓 History")
    if "messages" in st.session_state:
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"**Zoe:** {msg['content']}")
    else:
        st.write("No messages yet.")
