from telebot.apihelper import send_message
from credentials import BOT_TOKEN
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from db import db
import telebot

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_my_commands([
    BotCommand("start", "Start up the bot")
])

@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    start_message = ""

    # Sets up a Collection for the Group if there is none. Otherwise, proceed with the user side.
    if message.chat.type == "group":
        if db.project.find_one({"group_id": chat_id}) == None:
            db.project.insert_one({
                "group_id": chat_id,
                "group_name": message.chat.title
            })
        start_message += "The bot had been set up for the group. Please set it up from the user side."
        bot.send_message(chat_id, start_message)
        return

    elif message.chat.type == "private":
        if len(list(db.project.find())) == 0:
            start_message += "The bot has not been set up in a group yet."
            bot.send_message(chat_id, start_message)
            return

        else: 
            buttons = []
            for key in list(db.project.find()):
                row = []
                button = InlineKeyboardButton(key["group_name"], callback_data=f'Chosen Group {key["group_name"]}')
                row.append(button)
                buttons.append(row)
            start_message += "Select a group that you will be like to post in."
            bot.send_message(chat_id, start_message, reply_markup=InlineKeyboardMarkup(buttons))
            return

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
    # Error Handling
    if db.project.find_one({"group_name": group_name}) == None:
        bot.send_message(chat_id, "No such group found. Please activate the bot in the group.")
        return

    group_id = db.project.find_one({"group_name": group_name})["group_id"]
    bot.send_message(group_id, f'{user} is testing out the bot. Please bear with me')
    return


bot.infinity_polling()