from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os
import requests

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"
WEBHOOK_URL = "https://telegram-bot-3-0uhb.onrender.com/webhook"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# --- Komutlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif! Her şey yolunda.")

application.add_handler(CommandHandler("start", start))

# --- Webhook Route ---
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    loop = asyncio.get_event_loop()
    loop.create_task(application.process_update(update))
    return "ok", 200


@app.route('/')
def home():
    return "Bot is running!", 200


# --- Otomatik webhook ayarı ---
def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    response = requests.post(url, data=data)
    print("Webhook setleme sonucu:", response.text)


if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
