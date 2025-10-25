from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import os

# Telegram bot token (Render Environment Variable olarak BOT_TOKEN gir)
TOKEN = os.getenv("BOT_TOKEN", "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk")

# Flask uygulaması
app = Flask(__name__)

# Telegram bot uygulaması (asenkron)
application = ApplicationBuilder().token(TOKEN).build()


# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bot başarıyla çalışıyor 🚀")


# Normal mesaj geldiğinde
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Gönderdiğin mesaj: {update.message.text}")


# Komut ve mesaj handler’ları ekle
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# Telegram webhook endpoint’i
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok", 200


# Basit kontrol için ana sayfa
@app.route("/", methods=["GET"])
def home():
    return "Bot çalışıyor ✅"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
