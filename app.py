import streamlit as st
from agent.agent import PortfolioAgent

agent = PortfolioAgent()

st.title("⚡ Agent-AskStorm")
st.write("Ask anything about Kowshik's projects, skills, and experience")

if "messages" not in st.session_state or not isinstance(st.session_state.get("messages"), list):
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Ask something...")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Streamlit version keeps history in session_state; pass it to agent.
    response = agent.chat(prompt, st.session_state["messages"][:-1])

    st.chat_message("assistant").write(response)
    st.session_state["messages"].append({"role": "assistant", "content": response})