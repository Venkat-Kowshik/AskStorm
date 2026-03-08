from services.telegram_service import TelegramService

def record_user_details(email, name="Name not provided", notes="not provided"):

    message = f"""
📩 New Lead

Name: {name}
Email: {email}
Notes: {notes}
"""

    TelegramService.send(message)

    return {"recorded": "ok"}