from fastapi import APIRouter
import httpx
from openai import OpenAI
from pydantic import BaseModel
from services.llm import LLMChat
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

llm_router = APIRouter(tags=["LLM"])

llm_chat_instance = LLMChat()

# Define request and response models
class LLMRequest(BaseModel):
    message: str


@llm_router.post("/chat")
def chat_with_model(request: LLMRequest):
    try:
        llm_chat_instance.add_user_message(request.message)
        response_message = llm_chat_instance.generate_response()
        return {"response": response_message}
    except Exception as e:
        logger.error("Error in /chat endpoint: %s", str(e))
        return {"error": "An error occurred while processing your request."}

