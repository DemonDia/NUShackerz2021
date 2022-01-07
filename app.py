from pymongo import aggregation
from telebot.apihelper import send_message
from telebot import apihelper
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from db import db, BOT_TOKEN
import telebot

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_my_commands([
    BotCommand("start", "Start up the bot")
])

class User:
    def __init__(self):
        self.name = None
        self.gpa = None
        self.kink = None

user_dict = {}


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

        else:
            buttons = []
            for key in list(db.project.find()):
                row = []
                button = InlineKeyboardButton(key["group_name"], callback_data=f'Chosen Group {key["group_name"]}')
                row.append(button)
                buttons.append(row)
            start_message += "Select a group that you will be like to post in."
            bot.send_message(chat_id, start_message, reply_markup=InlineKeyboardMarkup(buttons))

def retrieve_user_info(chat_id):
    msg = bot.send_message(chat_id, "Hi! How do we address you?")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        name = message.text
        user = User(name)
        user_dict[message.chat.id] = user
        msg = bot.send_message(message.chat.id, "Write down your name")
        bot.register_next_step_handler(msg, process_gpa_step)

    except Exception as e:
        bot.reply_to(message, "Error!")

def process_gpa_step(message):
    try:
        gpa = message.text
        if not gpa.isdecimal():
            msg = bot.reply_to(message, "Please input your GPA in a decimal.")
            bot.register_next_step_handler(msg, process_gpa_step)

        if gpa < 0 or gpa > 4.0:
            msg = bot.reply_to(message, "Please input a valid GPA.")
            bot.register_next_step_handler(msg, process_gpa_step)

        user = user_dict[message.chat.id]
        user.gpa = gpa

        msg = bot.send_message(message.chat.id, "What secrets would you like to share?")
        bot.register_next_step_handler(msg, process_kink_step)

    except Exception as e:
        bot.reply_to(message, "Error!")
        
def process_kink_step(message):
    try:
        kink = message.text
        user = user_dict[message.chat.id]
        bot.send_message(message.chat.id, "Information saved successfully! Thanks for filling up the information")

    except Exception as e:
        bot.reply_to(message, "Error!")







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
    bot.send_message(chat_id, f'You have chosen the group {group_name} to post the images.')
    retrieve_user_info(chat_id)
    return


bot.infinity_polling()
