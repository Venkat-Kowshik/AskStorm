import json
from pypdf import PdfReader

from services.llm_service import LLMService
from tools.record_user import record_user_details
from tools.record_question import record_unknown_question
from agent.prompts import system_prompt


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

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "record_user_details",
                    "description": "Record user contact information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "name": {"type": "string"},
                            "notes": {"type": "string"}
                        },
                        "required": ["email"]
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

        messages = [
            {
                "role": "system",
                "content": system_prompt(self.name, self.summary, self.linkedin)
            }
        ]

        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        messages.append({
            "role": "user",
            "content": message
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

                    record_unknown_question(message)

                    reply += "\n\nI'm curious though — what made you ask that? Also may I know your name?"

                return reply