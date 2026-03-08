from groq import Groq
from config.settings import settings

class LLMService:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, messages, tools):

        return self.client.chat.completions.create(
            model=settings.MODEL,
            messages=messages,
            tools=tools
        )