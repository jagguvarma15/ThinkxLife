# advanced_ui.py
import streamlit as st
import os
import streamlit.components.v1 as components

AVATAR_USER = "assets/user.png"
AVATAR_BOT = "assets/zoe.png"

# Render a single chat message with optional highlight
def render_chat_message(role, content, highlight=False):
    bubble_class = "bot" if role == "assistant" else "user"
    avatar_path = AVATAR_BOT if role == "assistant" else AVATAR_USER
    wrapper_class = f"message-wrapper {bubble_class}"
    highlight_style = "background-color: #fff3cd; border: 2px solid #f0ad4e;" if highlight else ""

    with st.container():
        st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
        cols = st.columns([1, 12]) if role == "assistant" else st.columns([12, 1])

        with cols[0 if role == "assistant" else 1]:
            try:
                st.image(avatar_path, width=32)
            except:
                st.markdown("🤖" if role == "assistant" else "🧍")

        with cols[1 if role == "assistant" else 0]:
            align_style = "text-align: right;" if role != "assistant" else ""
            st.markdown(
                f"<div class='chat-bubble {bubble_class}' style='{align_style}; {highlight_style}'>{content}</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

# Render full chat message block with scroll & highlight
def render_styled_chat():
    st.markdown('<div class="custom-chat-container">', unsafe_allow_html=True)
    for idx, message in enumerate(st.session_state.messages):
        anchor_id = f"msg-{idx}"
        if idx == st.session_state.get("scroll_to_index"):
            st.markdown(f"<div id='{anchor_id}'></div>", unsafe_allow_html=True)

    if st.session_state.get("scroll_to_index") is not None:
        scroll_id = f"msg-{st.session_state.scroll_to_index}"
        st.components.v1.html(f"""
            <script>
                window.addEventListener("load", function() {{
                    const el = document.getElementById("{scroll_id}");
                    if (el) {{
                        el.scrollIntoView({{ behavior: "smooth", block: "center" }});
                    }}
                }});
            </script>
        """, height=0)
        highlight_idx = st.session_state.scroll_to_index
        st.session_state.scroll_to_index = None
    else:
        highlight_idx = None

    last_index = len(st.session_state.messages) - 1

    for idx, message in enumerate(st.session_state.messages):
        render_chat_message(message["role"], message["content"], highlight=(idx == highlight_idx))

    st.markdown("<div id='msg-end'></div>", unsafe_allow_html=True)
    inject_auto_scroll()

def inject_auto_scroll():
    components.html("""
        <script src="/ui/js/scroll.js"></script>
    """, height=0)

# Optional: Wrap the whole chat area
def start_chat_container():
    st.markdown('<div class="custom-chat-container">', unsafe_allow_html=True)

def end_chat_container():
    st.markdown('</div>', unsafe_allow_html=True)
