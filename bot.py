from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading
import os
import asyncio

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif! Webhook bağlantısı başarılı 🔥")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ /start yazarak botu test edebilirsin.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

def process_update_thread(data):
    async def process():
        await application.initialize()
        update = Update.de_json(data, bot)
        await application.process_update(update)

    asyncio.run(process())

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        threading.Thread(target=process_update_thread, args=(data,)).start()
        return "ok", 200
    except Exception as e:
        print("Webhook hatası:", e)
        return "error", 500

@app.route("/")
def home():
    return "🚀 Telegram Bot aktif (Flask + Render)", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
