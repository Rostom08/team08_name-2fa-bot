import telebot
import pyotp
from faker import Faker
from flask import Flask, request

# কনফিগারেশন
TOKEN = "8740612328:AAEi6KFoVytwFlCT0LiWOjmCD0claIEbcrc"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
fake = Faker()

# স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("🇧🇩 Bangladeshi Female Name", "🇺🇸 USA Female Name", "🔐 Get 2FA Code", "📧 Check Hotmail Inbox")
    bot.reply_to(message, "স্বাগতম! আমি একটি Multifunctional Bot! আপনার কি প্রয়োজন?", reply_markup=markup)

# নাম জেনারেশন
@bot.message_handler(func=lambda message: "Name" in message.text)
def generate_name(message):
    name = fake.name_female() if "Female" in message.text else fake.name()
    bot.reply_to(message, f"✅ Name: {name}")

# 2FA জেনারেটর
@bot.message_handler(func=lambda message: "2FA" in message.text)
def ask_2fa(message):
    msg = bot.reply_to(message, "আপনার 2FA Secret Key টি দিন:")
    bot.register_next_step_handler(msg, process_2fa)

def process_2fa(message):
    try:
        totp = pyotp.TOTP(message.text.strip())
        code = totp.now()
        bot.reply_to(message, f"🔐 Your Live 2FA Code: `{code}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ ভুল কী (Key)! দয়া করে সঠিক Secret Key দিন।")

# Hotmail Inbox (Placeholder)
@bot.message_handler(func=lambda message: "Inbox" in message.text)
def check_inbox(message):
    bot.reply_to(message, "📧 Hotmail Inbox কানেক্ট করা হয়েছে। দয়া করে আপনার লগইন ডিটেইলস দিন।")

# Vercel Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

if __name__ == "__main__":
    app.run()
