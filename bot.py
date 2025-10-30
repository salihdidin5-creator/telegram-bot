from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"
WEBHOOK_URL = "https://telegram-bot-3-0uhb.onrender.com/webhook"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# ---- KOMUTLAR ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif ve çalışıyor!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Komutlar:\n/start - Botu başlat\n/help - Yardım menüsü")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# ---- FLASK ROUTELARI ----
@app.route("/")
def home():
    return "🤖 Telegram bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

# ---- UYGULAMAYI ÇALIŞTIR ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
