from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import requests
import os

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"  # 🔹 senin bot tokenin
WEBHOOK_URL = "https://telegram-bot-3-0uhb.onrender.com/webhook"  # 🔹 senin Render adresin

app = Flask(__name__)

# Telegram uygulaması
application = ApplicationBuilder().token(TOKEN).build()

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif ve çalışıyor!")

application.add_handler(CommandHandler("start", start))

# Telegram webhook işlemi
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
        return "ok", 200
    return "error", 400

# Basit test sayfası
@app.route("/")
def home():
    return "Bot aktif ✅"

if __name__ == "__main__":
    # Webhook’u Telegram’a tanıt
    set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(set_webhook_url)
    print("Webhook kurulumu sonucu:", response.json())

    # Flask’ı başlat
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
