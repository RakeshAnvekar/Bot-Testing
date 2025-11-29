import os
from fastapi import FastAPI, Request, Response
from botbuilder.schema import Activity
import logging
from bot.adapter import adapter
from bot.bot import TeamsBot
from routes.llm_route import llm_router

logger = logging.getLogger(__name__)

app = FastAPI()

bot = TeamsBot()

app.include_router(llm_router)

@app.post("/api/messages")
async def messages(request: Request):
    """Main message endpoint for the bot."""
    try: 
        if "application/json" in request.headers.get("Content-Type", ""):
            body = await request.json()
        else:
            return Response(status_code=415)

        activity = Activity().deserialize(body)
        auth_header = request.headers.get("Authorization")
        return await adapter.process(request, bot)
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return Response(status_code=500, content=str(e))


@app.get("/")
def read_root():
    return {
        "message": "AI teams bot",
        "version": "1.0.0",
        "description": "This is an AI-powered Teams bot using FastAPI and Bot Framework."
    }