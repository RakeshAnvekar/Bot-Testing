from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

APP_ID = os.getenv("MICROSOFT_APP_ID")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")

if not APP_ID or not APP_PASSWORD:
    logger.error("MICROSOFT_APP_ID or MICROSOFT_APP_PASSWORD environment variable not set.")

settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

async def on_error(context, error):
    logger.error(f"Bot Error: {error}")
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity("To continue to run this bot, please fix the bot source code.")
adapter.on_turn_error = on_error
