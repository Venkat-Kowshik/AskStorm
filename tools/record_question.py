from services.telegram_service import TelegramService

def record_unknown_question(question):

    message = f"""
❓ Unknown Question

{question}
"""

    TelegramService.send(message)

    return {"recorded": "ok"}