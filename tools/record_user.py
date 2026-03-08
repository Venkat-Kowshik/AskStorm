from services.telegram_service import TelegramService

def record_user_details(email="", phone="", name="Name not provided", notes="not provided"):

    email = (email or "").strip()
    phone = (phone or "").strip()
    name = (name or "Name not provided").strip()
    notes = (notes or "not provided").strip()

    if not email and not phone:
        return {"recorded": "skipped", "reason": "no_contact_details"}

    message = f"""
📩 New Lead

Name: {name}
Email: {email}
Phone: {phone}
Notes: {notes}
"""

    TelegramService.send(message)

    return {"recorded": "ok"}