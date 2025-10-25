from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging
import os

# Token ortam değişkeninden alınır (Render'da tanımlanacak)
TOKEN = os.environ.get("8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk

")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Loglama
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dispatcher oluştur
dispatcher = Dispatcher(bot, None, workers=0)

# --- Komutlar ---
def start(update: Update, context):
    update.message.reply_text("Merhaba! Bot başarıyla çalışıyor 🚀")

def help_command(update: Update, context):
    update.message.reply_text("Kullanabileceğin komutlar: /start ve /help")

def echo(update: Update, context):
    update.message.reply_text("Bu komutu anlayamadım 🤖")

# Handler'lar
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# --- Webhook endpoint ---
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# --- Test endpoint ---
@app.route('/')
def index():
    return "Bot çalışıyor ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
