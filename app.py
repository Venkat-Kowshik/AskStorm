import streamlit as st
import time
from agent.agent import PortfolioAgent

agent = PortfolioAgent()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AskStorm AI",
    page_icon="⚡",
    layout="wide"
)

# ---------- CUSTOM CSS ----------st.markdown("""
st.markdown("""
<style>

/* App background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0f0c29, #0b0b1a);
    color: #E0E7FF;
}

/* Header styling */
h1 {
    color: #00F5FF;
    text-shadow: 0 0 4px #00F5FF ; 
}

/* Caption text */
.css-1d391kg {
    color: #A78BFA;
}

/* Chat messages */
.stChatMessage {
    border-radius: 12px;
    padding: 10px;
    background: rgba(20, 20, 40, 0.8);
    border: 1px solid #6D28D9;
    box-shadow: 0 0 12px rgba(168,85,247,0.5);
}

/* Buttons */
button {
    background: linear-gradient(90deg, #4C1D95, #22D3EE);
    color: #F9FAFB;
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.4);
    box-shadow: 0 0 4px rgba(15, 23, 42, 0.6);
}

/* Button hover */
button:hover {
    background: linear-gradient(90deg, #1E293B, #0F172A); /* much darker */
    color: #F9FAFB;                                       /* force light text */
    box-shadow: 0 0 6px rgba(15, 23, 42, 0.8);
}

/* Suggested prompt buttons */
div.stButton > button {
    width: 100%;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: #060613;
    border-right: 1px solid #7C3AED;
}

/* Profile image styling */
.sidebar-profile img {
  #  width: 120px;          /* same width & height => circle */
  #  height: 150px;
    border-radius: 50%;    /* makes it circular */
    object-fit: cover;     /* crops to a circle nicely */
    box-shadow:
        0 0 10px #00F5FF,
        0 0 20px #7C3AED,
        0 0 30px #EC4899;
}

/* Container spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)
# ---------- HEADER ----------
st.title("⚡ AskStorm AI")
st.caption("Your AI guide to Kowshik's projects, skills, and technical expertise")

# ---------- SIDEBAR ----------
with st.sidebar:
 
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    st.image("agent/assets/profile.png", width=180,)
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("👨‍💻 Venkata Sai Kowshik")

    st.write("""
AI Engineer | Cloud | Automation  

AskStorm AI is a conversational assistant trained on my projects, skills, and experience.
""")

    st.divider()

    st.subheader("🔗 Connect With Me")

    col1, col2 = st.columns(2)

    with col1:
        st.link_button(
            "LinkedIn",
            "https://www.linkedin.com/in/venkata-sai-kowshik-144984230/"
        )

    with col2:
        st.link_button(
            "GitHub",
            "https://github.com/Venkat-Kowshik"
        )

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- CHAT HISTORY ----------
for msg in st.session_state.messages:

    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"], unsafe_allow_html=True)

# ---------- SUGGESTED PROMPTS ----------
st.markdown("### 💡 Suggested Questions")

suggestions = [
    "What projects has Kowshik worked on?",
    "What technologies does Kowshik know?",
    "Tell me about the Recent project you have worked on",
    "What cloud technologies does Kowshik use?"
]

col1, col2 = st.columns(2)

for i, suggestion in enumerate(suggestions):

    if (col1 if i % 2 == 0 else col2).button(suggestion):

        st.session_state["prompt"] = suggestion

# ---------- CHAT INPUT ----------
prompt = st.chat_input("Ask something about Kowshik...")

if "prompt" in st.session_state:
    prompt = st.session_state.pop("prompt")

# ---------- PROCESS MESSAGE ----------
if prompt:

    # show user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # assistant response
    with st.chat_message("assistant", avatar="🤖"):

        thinking = st.empty()
        thinking.markdown("🤖 *AskStorm is thinking...*")

        response = agent.chat(prompt, st.session_state.messages[:-1])

        thinking.empty()

        message_placeholder = st.empty()
        full_response = ""

        # ---------- SMART RENDERING ----------
        if "|" in response and "---" in response:
            message_placeholder.markdown(response, unsafe_allow_html=True)
            full_response = response
        else:
            for word in response.split():
                full_response += word + " "
                time.sleep(0.09)
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

            message_placeholder.markdown(full_response, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })