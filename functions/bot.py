import telebot
import pyotp
import random
import requests
from faker import Faker
from flask import Flask, request

TOKEN = "8740612328:AAEi6KFoVytwFlCT0LiWOjmCD0claIEbcrc"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
fake = Faker()

# --- সুন্দর স্টাইলিশ নাম জেনারেটর ---
def get_styled_name():
    # রেশিও: ৩০% Male (0.0 - 0.3), ৭০% Female (0.3 - 1.0)
    gender = 'male' if random.random() < 0.3 else 'female'
    name = fake.name_male() if gender == 'male' else fake.name_female()
    
    # স্টাইলিশ বক্স ফরম্যাট
    return f"""
╔════════════════════════╗
      ✨ New Name Found
╚════════════════════════╝
👤 **Name:** `{name}`
⚧ **Gender:** {gender.capitalize()}
╔════════════════════════╝
"""

# --- ইমেইল কোড API ফাংশন ---
def get_code_from_dongvan(email, refresh_token, client_id, service_type):
    url = "https://tools.dongvanfb.net/api/get_code_oauth2"
    payload = {"email": email, "refresh_token": refresh_token, "client_id": client_id, "type": service_type}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json() if response.status_code == 200 else {"error": "API response error"}
    except:
        return {"error": "Connection Timeout"}

# --- বট হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Generate Name", "🔐 2FA Code", "📧 Get Mail Code")
    bot.reply_to(message, "স্বাগতম! আপনার কাঙ্ক্ষিত অপশনটি বেছে নিন:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👤 Generate Name")
def name_generator(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔄 Generate Again", callback_data="gen_name"))
    bot.reply_to(message, get_styled_name(), reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "gen_name")
def callback_gen(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=get_styled_name(), reply_markup=call.message.reply_markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🔐 2FA Code")
def ask_2fa(message):
    msg = bot.reply_to(message, "আপনার 2FA Secret Key টি দিন:")
    bot.register_next_step_handler(msg, process_2fa)

def process_2fa(message):
    try:
        key = message.text.strip()
        totp = pyotp.TOTP(key)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔄 Generate Again", callback_data=f"2fa_{key}"))
        bot.reply_to(message, f"🔐 **Current Code:** `{totp.now()}`", reply_markup=markup, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ ভুল কী (Key)! সঠিক Secret Key দিন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith("2fa_"))
def callback_2fa(call):
    key = call.data.split("_")[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=f"🔐 **New Code:** `{pyotp.TOTP(key).now()}`", reply_markup=call.message.reply_markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "📧 Get Mail Code")
def ask_mail_info(message):
    bot.reply_to(message, "তথ্যটি এই ফরম্যাটে দিন:\n`email|refresh_token|client_id|type`", parse_mode="Markdown")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    app.run()
