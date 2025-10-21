from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Flask uygulaması
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram bot çalışıyor!"

# Telegram bot token (Render secret olarak ekleyebilirsin)
TOKEN = os.environ.get("8199299680:AAGUONCVNwZVhLtZb1Eq-8OIay7SsBN_U5w")

if TOKEN:
    # Telegram botu başlat
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Merhaba! Bot çalışıyor.")

    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))

    # Telegram botu arka planda çalıştır
    import threading
    threading.Thread(target=lambda: app_bot.run_polling(), daemon=True).start()
