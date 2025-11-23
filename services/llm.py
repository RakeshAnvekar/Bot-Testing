import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=OPENAI_API_KEY)

class LLMChat:
    """
    Reusable LLM Chat session
    Maintains conversation history and allows incremnetal messages
    """

    def __init__(self, max_tokens=1000):
        self.max_tokens = max_tokens
        self.messages = []

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def generate_response(self):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                max_tokens=self.max_tokens
            )
            assistant_message = response.choices[0].message.content.strip()
            self.add_assistant_message(assistant_message)
            return assistant_message
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            raise