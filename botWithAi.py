import os
from fastapi import FastAPI, HTTPException, Request
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, ActivityHandler
from botbuilder.schema import Activity
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables (such as Microsoft App ID and Password)
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Bot Framework Adapter
adapter_settings = BotFrameworkAdapterSettings(
    os.getenv("MICROSOFT_APP_ID"),  # Your Azure Bot App ID
    os.getenv("MICROSOFT_APP_PASSWORD")  # Your Azure Bot App Password
)
adapter = BotFrameworkAdapter(adapter_settings)

# Backend API URL
BACKEND_API_URL = os.getenv("BACKEND_API_URL")  # URL of your backend API for processing messages

# Pydantic Models
class UserMessage(BaseModel):
    message: str

class ModelResponse(BaseModel):
    response: str

# Your Bot logic
class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Get the incoming message from Teams
        user_message = turn_context.activity.text.strip()

        # Send the message to the backend API for processing
        backend_response = await self.call_backend_api(user_message)

        # Send the response back to Teams
        await turn_context.send_activity(backend_response)

    async def call_backend_api(self, user_message: str):
        # Send user message to your backend API and get the response
        async with httpx.AsyncClient() as client:
            response = await client.post(
                BACKEND_API_URL,  # Backend API URL where your model is hosted
                json={"message": user_message}  # The format may vary depending on your backend API
            )

        # Handle the response
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("response", "Sorry, I couldn't process your request.")
        else:
            return "Sorry, there was an error processing your request."

# Instantiate the bot
my_bot = MyBot()

# FastAPI route to handle messages from Azure Bot Service
@app.post("/api/messages")
async def messages(request: Request):
    # Deserialize the incoming activity from Azure Bot Service
    body = await request.json()
    activity = Activity().deserialize(body)

    # Process the activity with the bot
    try:
        response = await adapter.process_activity(activity, "", my_bot.on_turn)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "Bot service is up and running!"}
