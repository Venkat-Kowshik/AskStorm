import gradio as gr
from agent.agent import PortfolioAgent

agent = PortfolioAgent()

if __name__ == "__main__":

    gr.ChatInterface(
        agent.chat,
        type="messages"
    ).launch()