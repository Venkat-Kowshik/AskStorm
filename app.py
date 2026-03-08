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

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.stChatMessage {
    border-radius: 10px;
}

.hero-title {
    font-size:28px;
    font-weight:bold;
}

.hero-subtitle {
    font-size:16px;
    color:grey;
}

</style>
""", unsafe_allow_html=True)



# ---------- HEADER ----------
st.title("⚡ AskStorm AI")
st.caption("Your AI guide to Kowshik's projects, skills, and technical expertise")

# ---------- SIDEBAR ----------
st.markdown("""
    <style>
    .sidebar-profile img {
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 0 15px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)
with st.sidebar:
    

    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    st.image("agent/assets/profile.png", width=200)
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
    "Tell me about the Vehicle Intelligence System",
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
        # If response contains a Markdown table, render instantly
        if "|" in response and "---" in response:
            message_placeholder.markdown(response, unsafe_allow_html=True)
            full_response = response
        else:
            # typing animation for normal text
            for word in response.split():
                full_response += word + " "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

            message_placeholder.markdown(full_response, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })