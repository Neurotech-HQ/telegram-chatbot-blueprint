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
# Set up Sarufi and get bot's name
sarufi = Sarufi(client_id=os.environ["sarufi_client_id"], client_secret=os.environ["sarufi_client_secret"])
bot_name=sarufi.get_bot(os.environ["sarufi_bot_id"]).name


# initialize the logger
logger = logging.getLogger()

##### HELPER FUCTIONS ####
def get_buttons(data:dict,type:str)->list:
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


def get_clicked_button_text(buttons:tuple,button_callback_data:str)-> str:
  for button in buttons:
    if button[0].callback_data==button_callback_data:
      return button[0].text


async def send_medias(update: Update,context: CallbackContext,media:dict,type:str):
  chat_id=update.effective_chat.id
  
  for file in media:
    url=file.get("link")
    caption=file.get("caption")
    
    if type=="images":
      response = requests.get(url)
      await context.bot.send_photo(chat_id=chat_id, photo=response.content,caption=caption)

    elif type=="audios":
      response = requests.get(url)
      await context.bot.send_audi(chat_id=chat_id, audio=response.content,caption=caption)
    
    elif type=="videos":
      response = requests.get(url)
      await context.bot.send_video(chat_id=chat_id, video=response.content,caption=caption)
    

    elif type=="documents":
      response = requests.get(url)
      await context.bot.send_document(chat_id=chat_id, document=response.content,caption=caption)


    elif type=="stickers":
      response = requests.get(url)
      await context.bot.send_stickers(chat_id=chat_id, sticker=response.content,caption=caption)

    else:
      logging.error(f"Sorry unrecognized media {type}")


async def respond(message, chat_id,message_type="text")->dict:
  """
  Responds to the user's message.
  """
  response = sarufi.chat(os.environ["sarufi_bot_id"], chat_id, message,channel="whatsapp",message_type= message_type)
  response = response.get("actions")
  return response


async def simulate_typing(update: Update, context: CallbackContext)->None:
  await context.bot.send_chat_action(
      chat_id=update.effective_chat.id, action=telegram.constants.ChatAction.TYPING
  )
  time.sleep(0.3)


async def reply_with_typing(update: Update, context: CallbackContext, message)->None:
    
  await simulate_typing(update, context)
  chat_id=update.effective_chat.id
  
  if isinstance(message,dict) or isinstance(message,list):

    for action in reversed(message):
      if action.get("send_message") and not action["send_message"]==['']:
        message = action.get("send_message")

        if isinstance(message, list):
            message = "\n".join(message)
        await context.bot.send_message(chat_id=chat_id, text=message)
      
      elif action.get("send_reply_button"):
        reply_button = action.get("send_reply_button")
        message=reply_button.get("body").get("text")
        buttons= get_buttons(reply_button.get("action"),"reply_button")              
        markdown=InlineKeyboardMarkup(buttons)

        await context.bot.send_message(chat_id=chat_id, text=message,reply_markup=markdown)

      elif action.get("send_button"):
        buttons=action.get("send_button")
        message=buttons.get("body")
        menus= get_buttons(buttons.get("action"),"button")
        markdown=InlineKeyboardMarkup(menus)

        await context.bot.send_message(chat_id=chat_id, text=message,reply_markup=markdown)

      elif action.get("send_images"):
        images=action.get("send_images")
        await send_medias(update,context,images,"images")

      elif action.get("send_videos"):
        videos=action.get("send_videos")
        await send_medias(update,context,videos,"videos")

      elif action.get("send_audios"):
        audios=action.get("send_audios")
        await send_medias(update,context,audios,"audios")

      elif action.get("send_documents"):
        documents=action.get("send_documents")
        await send_medias(update,context,documents,"documents")

      elif action.get("send_stickers"):
        stickers=action.get("send_stickers")
        await send_medias(update,context,stickers,"stickers")

      else:
        logger.error("Unkown action")

  else:
    await context.bot.send_message(chat_id=chat_id, text=message)


####### HANDLERS ##########
async def start(update: Update, context: CallbackContext)->None:
  """
  Starts the bot.
  """
  first_name = update.message.chat.first_name
  await reply_with_typing(
      update,
      context,
      os.environ["start_message"].format(name=first_name,bot_name=bot_name),
  )


async def help(update: Update, context: CallbackContext)->None:
  """
  Shows the help message.
  """
  await reply_with_typing(update, context, "Help message")


async def echo(update: Update, context: CallbackContext)->None:
  """
  Handles messages sent to the bot.
  """
  chat_id = update.message.chat.id
  response = await respond(update.message.text, chat_id)
  await reply_with_typing(update, context, response)


async def button_click(update: Update, context: CallbackContext)->None:
  query = update.callback_query
  buttons=query.message.reply_markup.inline_keyboard
  message=query.data
  button_text = get_clicked_button_text(buttons,message)
  context.user_data["selection"] = button_text
  chat_id=update.effective_chat.id

  await context.bot.send_message(chat_id=chat_id, 
                                  text=button_text, 
                                  reply_markup=ReplyKeyboardRemove(), 
                                  reply_to_message_id=query.message.message_id
                                  )

  response = await respond(message=message,
                            chat_id=chat_id, 
                            message_type="interactive"
                            )
  await reply_with_typing(update, context, response)


async def error(update: Update, context: CallbackContext)->None:
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, context.error)


#### MAIN FUNC ######
def main()->None:
  mybot= ApplicationBuilder().token(os.environ["token"]).build()
  
  mybot.add_handler(CommandHandler("start", start))
  mybot.add_handler(CommandHandler("help", help))
  mybot.add_handler(MessageHandler(filters.TEXT, echo))
  mybot.add_handler(CallbackQueryHandler(button_click))
  mybot.add_error_handler(error)

  mybot.run_polling()


if __name__ == "__main__":
  print("Starting bot...")
  main()