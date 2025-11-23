import logging
from botbuilder.core import TurnContext, ActivityHandler
from services.llm import LLMChat
from botbuilder.schema import ChannelAccount

logger = logging.getLogger(__name__)

llm_chat = LLMChat()

class TeamsBot(ActivityHandler):
    def __init__(self):
        logger.info("Initializing TeamsBot with LLMChat")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        logger.info(f"Received message from user: {user_message}")

        llm_chat.add_user_message(user_message)
        try:
            reply = llm_chat.generate_response()
            await turn_context.send_activity(reply)
            logger.info(f"Sent response to user: {reply}")
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            await turn_context.send_activity("Sorry, I encountered an error while processing your request.")

    async def on_members_added_activity(
        self,
        members_added: list[ChannelAccount],
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_text = "Hello and welcome! I am your AI assistant. How can I help you today?"
                await turn_context.send_activity(welcome_text)