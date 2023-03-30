import os
import time
import logging
import requests
import telegram
from sarufi import Sarufi
from dotenv import load_dotenv
from telegram import (
Update,
InlineKeyboardButton, 
InlineKeyboardMarkup,
ReplyKeyboardRemove
)
from telegram.ext import (
  CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ApplicationBuilder,
    CallbackQueryHandler
)

# load .env 
load_dotenv()
# Set up Sarufi
sarufi = Sarufi(os.environ["sarufi_username"], os.environ["sarufi_password"])
bot_name=sarufi.get_bot(os.environ["sarufi_bot_id"]).name


# initialize the logger
logger = logging.getLogger()


async def respond(message, chat_id)->dict:
    """
    Responds to the user's message.
    """
    response = sarufi.chat(os.environ["sarufi_bot_id"], chat_id, message,channel="whatsapp")
    response = response.get("actions")
    return response


async def simulate_typing(update: Update, context: CallbackContext):
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=telegram.constants.ChatAction.TYPING
    )
    time.sleep(0.3)

def get_buttons(data:dict,type:str):
  buttons=[]
  if type=="reply_button":
    for button in data.get("buttons"):
      button_title=button.get("reply").get("title")
      button_id=button.get("reply").get("id")
      button_data=[InlineKeyboardButton(button_title,callback_data=button_id)]
      buttons.append(button_data)
    return buttons
  else:
    for menu in data.get("sections")[0].get("rows"):
      menu_title=menu.get("title")
      menu_id=menu.get("id")
      menu_button=[InlineKeyboardButton(menu_title,callback_data=menu_id)]
      buttons.append(menu_button)
    return buttons

async def reply_with_typing(update: Update, context: CallbackContext, message):
    await simulate_typing(update, context)

    if isinstance(message,dict) or isinstance(message,list):

        for action in message:
            if action.get("send_message") and not action["send_message"]==['']:
                message = action.get("send_message")
                if isinstance(message, list):
                    message = "\n".join(message)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            
            elif action.get("send_reply_button"):
                reply_button = action.get("send_reply_button")
              
                message=reply_button.get("body").get("text")
                buttons= get_buttons(reply_button.get("action"),"reply_button")              
                markdown=InlineKeyboardMarkup(buttons)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message,reply_markup=markdown)

            elif action.get("send_button"):
                buttons=action.get("send_button")
                message=buttons.get("body")
                menus= get_buttons(buttons.get("action"),"button")
                markdown=InlineKeyboardMarkup(menus)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message,reply_markup=markdown)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# handlers
async def start(update: Update, context: CallbackContext):
    """
    Starts the bot.
    """
    first_name = update.message.chat.first_name
    await reply_with_typing(
        update,
        context,
        os.environ["start_message"].format(name=first_name,bot_name=bot_name),
    )


async def help(update: Update, context: CallbackContext):
    """
    Shows the help message.
    """
    await reply_with_typing(update, context, "Help message")


async def echo(update: Update, context: CallbackContext):
    """
    Echoes the user's message.
    """
    chat_id = update.message.chat.id
    response = await respond(update.message.text, chat_id)
    await reply_with_typing(update, context, response)


async def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main()->None:
    mybot= ApplicationBuilder().token(os.environ["token"]).build()
    
    mybot.add_handler(CommandHandler("start", start))
    mybot.add_handler(CommandHandler("help", help))
    mybot.add_handler(MessageHandler(filters.TEXT, echo))
    mybot.add_error_handler(error)

    mybot.run_polling()

if __name__ == "__main__":
    print("Starting bot...")
    main()
