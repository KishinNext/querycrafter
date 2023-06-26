import logging
import traceback

from fastapi import APIRouter, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

from agents.general_agent import GeneralAgent
from utils.config_loaders import (
    get_config
)
from utils.config_loaders import get_secrets
from utils.database import create_db_session

config = get_config()
secrets = get_secrets(config)

engine = create_db_session(secrets['database']['url'])
agent = GeneralAgent(engine=engine, verbose=True)

SLACK_BOT_TOKEN = secrets['slack']['slack_bot_token']
SLACK_SIGNING_SECRET = secrets['slack']['slack_signing_secret']
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

router = APIRouter()
handler = SlackRequestHandler(app)


def execute_general_agent(text, say) -> str:
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        say: function to send a response to the channel.
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    try:
        response = agent.handle_request(text)
        return response
    except Exception as e:
        logging.error('Error occurred when executing the general agent: %s', str(e))
        logging.error('traceback: %s', traceback.format_exc())
        say("Agent error. Please try again.")
        return 'Agent error. Please try again.'


def get_body_question(body, say) -> str:
    """
    Function to get the text from the body of the request.
    Args:
        body: The body of the request.
        say: function to send a response to the channel.

    Returns: The text from the body of the request.
    """
    try:
        text = body["event"]["text"]
        return text
    except KeyError as e:
        logging.error('KeyError occurred when processing the body: %s', str(e))
        logging.error('traceback: %s', traceback.format_exc())
        say("I'm sorry, there was an error processing your message.")
        return 'There was an error processing your message. no text found in body'


@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = get_body_question(body, say)
    logging.info(f"Received message: {text}")
    response = execute_general_agent(text, say)
    logging.info(f"Response Agent: {response}")
    say(response)


@router.post("/events")
async def slack_events(req: Request):
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return await handler.handle(req)


@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")
