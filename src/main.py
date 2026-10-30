import argparse
import logging

from src.aws.s3 import ensure_bucket_exists, s3_client
from src.features.llm_chat.client import LLMChatClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(message: str):
    ensure_bucket_exists()
    chat_client = LLMChatClient(s3_client)
    return chat_client.chat(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Chat Client")
    parser.add_argument(
        "message",
        type=str,
        help="The message to send to the LLM chat client",
    )
    args = parser.parse_args()
    message = args.message
    logger.info(f"Sending message to LLM chat client: {message}")
    response = main(message)
    logger.info(f"Response from LLM chat client: {response}")
