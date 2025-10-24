from flask import Flask, request
from telegram import Bot, Update
import os

# Telegram Token'ınızı Render secrets üzerinden ekleyin
TOKEN = os.environ.get("8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk")  # örn: "8199299680:AA...vQIk"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        
        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text

            # Basit cevap: gelen mesajı geri gönder
            bot.send_message(chat_id=chat_id, text=f"Sen: {text}")

    except Exception as e:
        print("Hata:", e)
    return "ok"

# Ana sayfa
@app.route("/")
def index():
    return "Telegram bot çalışıyor!"
