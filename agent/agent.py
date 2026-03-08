import json
import re
from datetime import datetime, timezone

from pypdf import PdfReader

from agent.prompts import system_prompt
from services.llm_service import LLMService
from tools.record_question import record_unknown_question
from tools.record_user import record_user_details

class PortfolioAgent:

    def __init__(self):

        self.name = "Venkata Sai Kowshik"

        self.llm = LLMService()

        reader = PdfReader("data/Profile.pdf")

        self.linkedin = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        with open("data/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

        self._notified_leads: set[str] = set()

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "record_user_details",
                    "description": "Record user contact information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "phone": {"type": "string"},
                            "email": {"type": "string"},
                            "name": {"type": "string"},
                            "notes": {"type": "string"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "record_unknown_question",
                    "description": "Record questions that cannot be answered",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"}
                        },
                        "required": ["question"]
                    }
                }
            }
        ]

    def handle_tool_call(self, tool_calls):

        results = []

        for tool_call in tool_calls:

            name = tool_call.function.name

            args = json.loads(tool_call.function.arguments)

            if name == "record_user_details":
                result = record_user_details(**args)

            elif name == "record_unknown_question":
                result = record_unknown_question(**args)

            else:
                result = {}

            results.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        return results

    def chat(self, message, history):
        user_text = _content_to_text(message)
        self._maybe_notify_interested_lead(user_text)

        messages = [
            {
                "role": "system",
                "content": system_prompt(self.name, self.summary, self.linkedin)
            }
        ]

        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": _content_to_text(msg.get("content"))
            })

        messages.append({
            "role": "user",
            "content": user_text
        })

        for _ in range(3):

            response = self.llm.generate(messages, self.tools)

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls":

                message = choice.message

                tool_calls = message.tool_calls

                results = self.handle_tool_call(tool_calls)

                messages.append(message)

                messages.extend(results)

            else:

                reply = choice.message.content

                if "I don't have information about that in my background" in reply:

                    record_unknown_question(user_text)

                    reply += "\n\nI'm curious though — what made you ask that? Also may I know your name?"

                return reply

    def _maybe_notify_interested_lead(self, user_text: str) -> None:
        lead = _extract_lead(user_text)
        if not lead:
            return

        key = (lead.get("email") or lead.get("phone") or "").strip().lower()
        if not key:
            return
        if key in self._notified_leads:
            return

        self._notified_leads.add(key)

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        notes_lines: list[str] = [
            f"Time: {timestamp}",
            "Message:",
            user_text.strip(),
        ]

        record_user_details(
            email=lead.get("email", ""),
            phone=lead.get("phone", ""),
            name=lead.get("name") or "Name not provided",
            notes="\n".join(notes_lines).strip() or "not provided",
        )


def _content_to_text(content) -> str:
    """
    Gradio 6 chat history uses structured content blocks.
    Normalize incoming `message` / `history[i]['content']` to plain text.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        # Sometimes content can be a single block: {"type": "text", "text": "..."}
        if content.get("type") == "text" and isinstance(content.get("text"), str):
            return content["text"]
        # Best-effort fallback
        return json.dumps(content, ensure_ascii=False)
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
                continue
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                parts.append(block["text"])
        if parts:
            return "\n".join(p.strip() for p in parts if p.strip())
        return json.dumps(content, ensure_ascii=False)

    return str(content)


_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_IN_PHONE_RE = re.compile(r"\b(?:\+?91[\s-]?)?([6-9]\d{9})\b")
_NAME_RE = re.compile(r"\b(?:i'm|im|i am|this is|my name is)\s+([A-Za-z][A-Za-z .'-]{1,50})\b", re.I)


def _extract_lead(text: str) -> dict[str, str] | None:
    if not text or not isinstance(text, str):
        return None

    lowered = text.lower()
    interest = any(
        kw in lowered
        for kw in (
            "reach out",
            "contact me",
            "call me",
            "text me",
            "email me",
            "connect",
            "collaborat",
            "work with",
            "partnership",
            "partner",
            "hire",
            "opportunity",
            "role",
            "position",
            "opening",
            "available",
            "let me know",
            "waiting for your reply",
        )
    )

    emails = _EMAIL_RE.findall(text)
    phones = _IN_PHONE_RE.findall(text)

    if not interest:
        return None
    if not emails and not phones:
        return None

    name_match = _NAME_RE.search(text)
    name = name_match.group(1).strip() if name_match else ""
    # Clean common suffixes like "- SDE-2 at Walmart"
    if " - " in name:
        name = name.split(" - ", 1)[0].strip()
    if "-" in name and len(name.split("-")[0].strip()) >= 2:
        name = name.split("-", 1)[0].strip()

    lead: dict[str, str] = {}
    if name:
        lead["name"] = name
    if emails:
        lead["email"] = emails[0]
    if phones:
        lead["phone"] = phones[0]

    return lead or None