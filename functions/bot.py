import telebot
import pyotp
from faker import Faker
from flask import Flask, request

TOKEN = "8740612328:AAEi6KFoVytwFlCT0LiWOjmCD0claIEbcrc"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
fake = Faker()

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def home():
    return 'Bot is active'
