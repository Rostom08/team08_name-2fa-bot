import telebot
import pyotp
from faker import Faker
from flask import Flask, request

TOKEN = "8740612328:AAEi6KFoVytwFlCT0LiWOjmCD0claIEbcrc"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
fake = Faker()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇧🇩 BD Name", "🇺🇸 USA Name", "🔐 2FA Code", "📧 Hotmail")
    bot.reply_to(message, "স্বাগতম! মেনু থেকে সিলেক্ট করুন:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🇧🇩 BD Name", "🇺🇸 USA Name"])
def generate_name(message):
    name = fake.name()
    bot.reply_to(message, f"✅ Name: {name}")

@bot.message_handler(func=lambda message: message.text == "🔐 2FA Code")
def ask_2fa(message):
    msg = bot.reply_to(message, "আপনার 2FA Secret Key টি দিন:")
    bot.register_next_step_handler(msg, process_2fa)

def process_2fa(message):
    try:
        totp = pyotp.TOTP(message.text.strip())
        bot.reply_to(message, f"🔐 Code: `{totp.now()}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ ভুল কী (Key)!")

@bot.message_handler(func=lambda message: message.text == "📧 Hotmail")
def check_inbox(message):
    bot.reply_to(message, "📧 Hotmail ইনবক্স সার্ভিসটি বর্তমানে মেইনটেন্যান্সে আছে।")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    app.run()
