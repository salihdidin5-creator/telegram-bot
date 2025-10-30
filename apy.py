from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import requests
import os

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"
WEBHOOK_URL = "https://telegram-bot-3-xxxx.onrender.com/webhook"  # senin Render URL’in

app = Flask(__name__)

# Telegram uygulaması
application = ApplicationBuilder().token(TOKEN).build()

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif ve çalışıyor!")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint — Telegram POST isteği buraya gelir
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok", 200

# Basit test sayfası (Render'ın GET isteği için)
@app.route("/")
def home():
    return "Bot aktif ✅", 200

if __name__ == "__main__":
    # Webhook'u Telegram'a tanıt
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
    print("Webhook kuruldu:", WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
