import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    class SlackNotifier:
        def __init__(self, token: str, channel: str):
            self.client = WebClient(token=token)
            self.channel = channel
            logger.info("SlackNotifier initialized.")

        def send_message(self, text: str):
            try:
                self.client.chat_postMessage(channel=self.channel, text=text)
                logger.info("Message sent to Slack.")
            except SlackApiError as e:
                logger.error(f"Slack API error: {e.response['error']}")
            except Exception as e:
                logger.exception(f"Unexpected error while sending Slack message: {e}")

except ImportError as e:
    logger.warning("slack_sdk not installed. SlackNotifier will be None.")
    SlackNotifier = None

# Initialize the notifier
SLAK_TOKEN = os.getenv("SLAK_TOKEN")
CHANNEL = os.getenv("CHANNEL")
notifier = SlackNotifier(SLAK_TOKEN, CHANNEL) if SlackNotifier else None
