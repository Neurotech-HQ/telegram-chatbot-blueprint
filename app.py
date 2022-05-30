# 5539985581:AAGwHSY4Phn3ORD7Xac8sNDj-eHlam8wvA8
import yaml
import time
import logging
import telegram
from sarufi import Sarufi
from telegram import Update
from telegram.ext import (
    CommandHandler,
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
)


def load_config():
    try:
        with open("config.yaml", "r") as f:
            config = yaml.load(f)
        return config
    except FileNotFoundError:
        print("Config file not found")
        exit(1)


config = load_config()

# Set up Sarufi
sarufi = Sarufi(config["sarufi"]["username"], config["sarufi"]["password"])

updater = Updater(sarufi["telegram"]["token"])
mybot = updater.dispatcher

# initialize the logger
logger = logging.getLogger()


def respond(message, chat_id):
    """
    Responds to the user's message.
    """
    response = sarufi.chat(message, chat_id)
    response = response["message"]
    return response


def simulate_typing(update: Update, context: CallbackContext):
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING
    )
    time.sleep(0.3)


def reply_with_typing(update: Update, context: CallbackContext, message):
    simulate_typing(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def start(update: Update, context: CallbackContext):
    """
    Starts the bot.
    """
    first_name = update.message.chat.first_name
    reply_with_typing(
        update,
        context,
        config["telegram"]["start_message"].format(name=first_name),
    )


def help(update: Update, context: CallbackContext):
    """
    Shows the help message.
    """
    reply_with_typing(update, context, "Help message")


def echo(update: Update, context: CallbackContext):
    """
    Echoes the user's message.
    """
    chat_id = update.message.chat.id
    response = respond(update.message.text, chat_id)
    reply_with_typing(update, context, response)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


mybot.add_handler(CommandHandler("start", start))
mybot.add_handler(CommandHandler("help", help))
mybot.add_handler(MessageHandler(Filters.text, echo))
mybot.add_error_handler(error)

if __name__ == "__main__":
    print("Starting bot...")
    updater.start_polling()
