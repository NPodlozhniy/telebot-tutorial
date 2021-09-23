import argparse
import os
import telebot
from flask import Flask, request
from dataloader import stats

BASE_URL = 'https://telebottutorial.herokuapp.com/'
TELEBOT_URL = 'telebot_webhook/'

API_TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(API_TOKEN)

SECRETNAME = os.environ.get("SECRETNAME")

server = Flask(__name__)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text='Yes',
                                                    callback_data='yes'))
    keyboard.add(telebot.types.InlineKeyboardButton(text='No',
                                                    callback_data='no'))
    bot.reply_to(message,
                 text="Hi there, I am an unofficial ZELF bot fot for the team! I can send you statistics for yesterday by the /stats command. Do you want to receive statistics?",
                 reply_markup=keyboard)


# Handle '/stats'
@bot.message_handler(commands=['stats'])
def send_stats(message):
    bot.send_message(message.chat.id, "Who is the Master of Humor?")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    if message.text == SECRETNAME:
        bot.send_message(message.chat.id, "A few moments...")
        bot.send_message(message.chat.id, stats())
    else:
        bot.send_message(message.chat.id, "Are you really a ZELF employee?")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, "If you want something other than yesterday's statistics, look for a better bot!")


# Handle pressing the button
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        send_stats(call.message)
    elif call.data == "no":
        echo_message(call.message)


# Server passes messages to the bot
@server.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
        

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
    return "!", 200


# Choose between webhook and polling mode depending on the command line argument
parser = argparse.ArgumentParser(description='Run the bot')
parser.add_argument('--local', action='store_true', help='run the bot in a local host')
args = parser.parse_args()

if args.local:
    bot.remove_webhook()
    bot.polling()
else:
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    webhook()