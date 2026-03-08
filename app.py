import gradio as gr
from agent.agent import PortfolioAgent
from services.telegram_service import TelegramService 
from services.llm_service import LLMService


agent = PortfolioAgent()

if __name__ == "__main__":

    gr.ChatInterface(
        agent.chat,
        title="AskStorm AI",
        description="Ask anything about Kowshik's projects, skills, and experience.",
    ).launch()