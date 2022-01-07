from telebot.apihelper import send_message
from telebot import apihelper
from credentials import BOT_TOKEN
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from db import db
import telebot

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_my_commands([
    BotCommand("start", "Start up the bot")
])

# handle_start(message)
# param[in] message: The message sent by the user.

@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    start_message = ""

    if message.chat.type != "private":
        if db.project.find_one({"group_id": chat_id}) == None:
            db.project.insert_one({
                "group_id": chat_id,
                "group_name": message.chat.title
            })
        start_message += "The bot had been set up for the group. Please set it up from the user side."
        bot.send_message(chat_id, start_message)
        return

    else:
        if len(list(db.project.find())) == 0:
            start_message += "The bot has not been set up in a group yet."
            bot.send_message(chat_id, start_message)
            return

    
        buttons = []
        for key in list(db.project.find()):
            row = []
            button = InlineKeyboardButton(key["group_name"], callback_data=f'Chosen Group {key["group_name"]}')
            row.append(button)
            buttons.append(row)
        start_message += "Select a group that you will be like to post in."
        bot.send_message(chat_id, start_message, reply_markup=InlineKeyboardMarkup(buttons))


###### Function used to handle Callback #########
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user = call.message.chat.first_name
    data = call.data

    intent = data.split()[0:][0]

    if intent == "Chosen":
        group_name = data.split()[0:][2]
        send_message_logic(chat_id, group_name, user)
        return

    return

def send_message_logic(chat_id, group_name, user):
    information = {"name": user}
    db.project.find_one_and_update({"group_name": group_name}, {"$set": {"user": information}})
    bot.send_message(chat_id, f'You have chosen the group {group_name} to post the images. To proceed with uploading of seccrets, type /secrets')
    return

@bot.message_handler(func=lambda message: message.text is not None, content_types=["text"])
def handle_text_doc(message):
    chat_id = message.chat.id

    if message.chat.type == "private":
        if "secret" not in message.text:
            bot.send_message(chat_id, "Sorry I do not understand the message")
            return
        else:
            bot.reply_to(message, f'Your secret of {message.text} had been stored')

bot.infinity_polling()
