from services.telegram_service import TelegramService
from services.llm_service import LLMService

class LeadService:

    @staticmethod
    def record_user(email, name, notes):

        message = f"""
📩 New Lead

Name: {name}
Email: {email}
Notes: {notes}
"""

        TelegramService.send(message)

    @staticmethod
    def record_question(question):

        message = f"""
❓ New Question Asked

{question}
"""

        TelegramService.send(message)