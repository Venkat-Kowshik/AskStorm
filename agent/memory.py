from services.llm_service import LLMService

class ConversationMemory:

    def __init__(self, system_prompt: str, max_history: int = 10):

        self.system_prompt = system_prompt
        self.max_history = max_history


    def build_messages(self, history, user_message):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        # Limit history size to avoid token overflow
        trimmed_history = history[-self.max_history:]

        for msg in trimmed_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages