import logging
import random
import pyotp
from faker import Faker
from fastapi import FastAPI, Request, Response
import telebot

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Configuration
BOT_TOKEN = "8740612328:AAEi6KFoVytwFlCT0LiWOjmCD0claIEbcrc"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
fake_us = Faker('en_US')

app = FastAPI()

# Data Lists
bd_first_names = ["Afia", "Samiya", "Mim", "Jannatul", "Rupa", "Puja", "Sadiya", "Fatema", "Tanjila", "Nusrat", "Mst", "Afrin", "Sumaiya", "Farhana", "Tasnim", "Anika", "Riya", "Sultana", "Fariha", "Sabrina", "Nabila", "Meherin", "Tisha", "Lamia", "Zarin", "Sharmin", "Khadija", "Marium", "Umme", "Ayesha", "Israt", "Nigar", "Rupali", "Nupur", "Nadia", "Farzana", "Sadia", "Tahmina", "Keya"]
bd_last_names = ["Shukla", "Akter", "Moni", "Hok", "Shen", "Roy", "Jahan", "Ferdous", "Khatun", "Islam", "Rahman", "Begum", "Khanam", "Chowdhury", "Das", "Hasan", "Tarafdar", "Biswas", "Tara", "Banu", "Nahar", "Alam", "Mimi", "Afroz", "Sharker", "Adhikary", "Sarkar", "Paul", "Majumder", "Ali"]

# Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🇧🇩 Bangladeshi Female Name", callback_data="gen_bd"))
    markup.add(telebot.types.InlineKeyboardButton("🇺🇸 USA Female Name", callback_data="gen_us"))
    bot.send_message(message.chat.id, "স্বাগতম! নাম জেনারেট করতে বাটন চাপুন:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_2fa(message):
    user_input = message.text.strip().replace(" ", "")
    try:
        live_code = pyotp.TOTP(user_input).now()
        bot.reply_to(message, f"🔐 Live 2FA Code: <code>{live_code}</code>", parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ ভুল 2FA Key! সঠিক কী পাঠান।")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "gen_bd":
        full_name = f"{random.choice(bd_first_names)} {random.choice(bd_last_names)}"
        bot.send_message(call.message.chat.id, f"🇧🇩 Name: <code>{full_name}</code>", parse_mode="HTML")
    elif call.data == "gen_us":
        full_name = f"{fake_us.first_name_female()} {fake_us.last_name()}"
        bot.send_message(call.message.chat.id, f"🇺🇸 Name: <code>{full_name}</code>", parse_mode="HTML")

# Webhook Route
@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.body()
    update = telebot.types.Update.de_json(data.decode('utf-8'))
    bot.process_new_updates([update])
    return Response(status_code=200)

@app.get("/")
async def root():
    return {"status": "Bot is active"}
