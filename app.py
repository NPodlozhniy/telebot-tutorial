import os
import telebot
import argparse
from flask import Flask, request

import config
import dbworker
from dataloader import stats, lifetime
from models import SetUp, Create, User, CreateUser, GetUser

BASE_URL = 'https://telebottutorial.herokuapp.com/'
TELEBOT_URL = 'telebot_webhook/'

API_TOKEN = os.environ.get("TOKEN")
SECRETNAME = os.environ.get("SECRETNAME")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Declare and configure statefull database
SetUp(app)
# Uncomment only on first first deployment
# Create()

buttons = [b"\xF0\x9F\x92\xB3".decode() + " Cards",
           b"\xF0\x9F\x92\xB6".decode() + " Transactions",
           b"\xE2\x9C\x85".decode() + " Verification"]

def keyboard_inline():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(
        telebot.types.InlineKeyboardButton(text='Yes', callback_data='yes'),
        telebot.types.InlineKeyboardButton(text='No', callback_data='no')
        )
    return keyboard


def keyboard_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.add(
        telebot.types.KeyboardButton(text=buttons[0]),
        telebot.types.KeyboardButton(text=buttons[1]),
        telebot.types.KeyboardButton(text=buttons[2])
        )
    return keyboard


def keyboard_remove():
    keyboard = telebot.types.ReplyKeyboardRemove()
    return keyboard


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    user = GetUser(message)
    if user is None:
        CreateUser(message)
    else:
        user.logout()
    dbworker.set_state(message.chat.id, config.states.init.value)
    bot.reply_to(message,
                text=f"Hi there, I am an unofficial ZELF bot for the team! I can send you statistics for yesterday by the /stats command. Do you want to receive statistics?",
                reply_markup=keyboard_inline())


# Handle '/stats'
@bot.message_handler(commands=['stats'])
def send_auth(message):
    user = GetUser(message)
    if user is None:
        CreateUser(message)
        user = GetUser(message)
    if dbworker.get_state(message.chat.id) == config.states.auth.value:
        send_options(message)
    elif user.state == config.states.auth.value:
        dbworker.set_state(message.chat.id, config.states.auth.value)
        send_options(message)
    else:
        bot.send_message(message.chat.id, "Who is the Master of Humor?")
        bot.register_next_step_handler(message, get_auth)


# If user is not authorize offer to athorize
def get_auth(message):
    if message.text.lower() == SECRETNAME.lower():
        user = GetUser(message)
        user.login()
        dbworker.set_state(message.chat.id, config.states.auth.value)
        send_options(message)
    else:
        bot.send_message(message.chat.id,
                         "Are you really a ZELF employee?",
                         reply_markup=keyboard_inline())


# If user is authorized send options
def send_options(message):
    bot.send_message(message.chat.id, "Choose one of the options below", reply_markup=keyboard_menu())


# Handle messages from authorized users
@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == config.states.auth.value)
def auth_message(message):
    if message.text == buttons[0]:
        bot.send_message(message.chat.id, "A few moments...")
        bot.send_message(message.chat.id, stats("Cards"))
    elif message.text == buttons[1]:
        bot.send_message(message.chat.id, "A few moments...")
        bot.send_message(message.chat.id, stats("Transactions"))
    elif message.text == buttons[2]:
        bot.send_message(message.chat.id, "A few moments...")
        bot.send_message(message.chat.id, stats("Verifications"))
    elif message.text.lower() == 'lifetime': # hidden function
        bot.send_message(message.chat.id, "A few moments...")
        bot.send_message(message.chat.id, lifetime())
    else:
        bot.send_message(message.chat.id, "If you want something other than yesterday's statistics, look for a better bot!")


# Handle sensitive messages from unauthorized users
@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == config.states.init.value)
def unauth_message(message):
    user = GetUser(message)
    if user is not None and user.state == config.states.auth.value:
        dbworker.set_state(message.chat.id, config.states.auth.value)
        auth_message(message)
    else:
        bot.send_message(message.chat.id,
                        "You need to pass the authorization to get statistics!",
                        reply_markup=keyboard_remove())


# Handle pressing the button
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        send_auth(call.message)
    elif call.data == "no":
        unauth_message(call.message)


# Server passes messages to the bot
@app.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
        

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
    return "!", 200


# Choose between webhook and polling mode depending on the command line argument
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run the bot')
    parser.add_argument('--local', action='store_true', help='run the bot in a local host')
    args = parser.parse_args()

    if args.local:
        bot.remove_webhook()
        bot.polling()
    else:
        app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
        webhook()