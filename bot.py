from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os
import requests

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"
WEBHOOK_URL = "https://telegram-bot-3-xxxx.onrender.com/webhook"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Komut örneği
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot çalışıyor ✅")

application.add_handler(CommandHandler("start", start))

@app.route("/")
def index():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

if __name__ == "__main__":
    app.run(port=10000)
