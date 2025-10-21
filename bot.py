from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters
import os

app = Flask(__name__)

# 🔹 Token (gerçek tokenini buraya yaz)
TOKEN = "YOUR_BOT_TOKEN_HERE"  # örnek:"8199299680:AAGUONCVNwZVhLtZb1Eq-8OIay7SsBN_U5w"

bot = Bot(token=TOKEN)

# 🔹 Chat ID (mesaj göndermek istersen)
CHAT_ID = "YOUR_CHAT_ID_HERE"  # örnek:"1211267625"

# 🔹 Dispatcher (gelen mesajları yönetir)
dispatcher = Dispatcher(bot, None, workers=0)

# 🔹 Komutlar
def start(update: Update, context):
    update.message.reply_text("Merhaba! Bot çalışıyor 🚀")

def echo(update: Update, context):
    update.message.reply_text(update.message.text)

# 🔹 Dispatcher’a handler ekle
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# 🔹 Flask webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running ✅", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
