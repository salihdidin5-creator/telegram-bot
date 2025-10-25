import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Telegram token
TOKEN = "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk"

# Flask app
app = Flask(__name__)

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Application
application = Application.builder().token(TOKEN).build()

# --- Komutlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! 👋")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Komutlar:\n/start - Botu başlat\n/help - Yardım menüsü")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# --- Handler'lar ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# --- Webhook route ---
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, application.bot)

        # initialize() ve start() çağrısı ekleniyor
        async def process():
            if not application._initialized:
                await application.initialize()
                await application.start()
            await application.process_update(update)

        asyncio.run(process())
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return "ok"


# --- Root test route ---
@app.route("/")
def home():
    return "Bot is running successfully!"


# --- Uygulama başlat ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
