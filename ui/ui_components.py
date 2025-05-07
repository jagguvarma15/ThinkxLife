import streamlit as st
import streamlit.components.v1 as components

AVATAR_USER = "assets/user.png"
AVATAR_BOT = "assets/zoe.png"

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

def render_styled_chat():
    st.markdown('<div class="custom-chat-container">', unsafe_allow_html=True)
    highlight_idx = st.session_state.get("scroll_to_index")

    for idx, message in enumerate(st.session_state.messages):
        anchor_id = f"msg-{idx}"
        st.markdown(f"<div id='{anchor_id}'></div>", unsafe_allow_html=True)
        render_chat_message(message["role"], message["content"], highlight=(idx == highlight_idx))

    # Auto-scroll only if needed, using safer API
    if highlight_idx is not None:
    # Inject anchor at top
        st.markdown(f"<a id='scroll-target' href='#msg-{highlight_idx}'></a>", unsafe_allow_html=True)

        # Auto-click it using safe JS trick
        st.markdown("""
        <script>
            setTimeout(() => {
                const anchor = document.getElementById("scroll-target");
                if (anchor) {
                    anchor.click();
                }
            }, 300);
        </script>
        """, unsafe_allow_html=True)

        st.session_state.scroll_to_index = None


def inject_auto_scroll():
    components.html("""
        <script>
            const chatEnd = window.parent.document.getElementById('msg-end');
            if (chatEnd) {
                chatEnd.scrollIntoView({ behavior: 'smooth' });
            }
        </script>
    """, height=0)

def render_profile_sidebar():
    state = st.session_state.state if "state" in st.session_state else {}
    name = state.get("name", "User")
    age = state.get("age", "N/A")

    st.markdown("""
    <style>
        .sidebar-card {
            background: #fdf6fb;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            font-family: 'Segoe UI', sans-serif;
        }
        .prompt-button {
            background-color: #fff;
            border: 1px solid #e0d7f4;
            border-radius: 10px;
            padding: 8px 12px;
            margin-bottom: 10px;
            font-size: 0.9rem;
            text-align: left;
            color: #4a4a4a;
            transition: all 0.2s ease-in-out;
            width: 100%;
        }
        .prompt-button:hover {
            background-color: #f3eaff;
            border-color: #c5b2e8;
            color: #333;
            cursor: pointer;
        }
        .sidebar-footer {
            position: fixed;
            bottom: 20px;
            left: 15px;
            font-size: 0.75rem;
            color: #aaa;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Profile Card ---
    st.markdown(f"""
    <div class="sidebar-card">
        <div style="font-size: 1.1rem;"><b>Name:</b> {name}</div>
        <div style="font-size: 1.1rem;"><b>Age:</b> {age}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Prompt History Tabs ---
    st.markdown("#### 📝 Your Prompts")
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            summary = msg["content"][:35] + ("..." if len(msg["content"]) > 35 else "")
            if st.button(f"🗨️ {summary}", key=f"scroll-btn-{idx}"):
                st.session_state.scroll_to_index = idx
                st.rerun()

    # --- Footer ---
    st.markdown("""
    <div class="sidebar-footer">
        © 2025 Think Round, Inc.
    </div>
    """, unsafe_allow_html=True)


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

def render_globe_button():
    st.markdown("""
        <style>
            .globe-button {
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: #f5f7fa;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 1.1rem;
                color: #0077cc;
                text-decoration: none;
                transition: all 0.2s ease-in-out;
                z-index: 1000;
            }
            .globe-button:hover {
                background: #e0ecf8;
                color: #005fa3;
            }
        </style>
        <a href="https://www.thinkround.org/" target="_blank" class="globe-button">🌐</a>
    """, unsafe_allow_html=True)
