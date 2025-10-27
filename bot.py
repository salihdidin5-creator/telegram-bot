from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"

app = Flask(__name__)

# Telegram bot uygulaması
application = ApplicationBuilder().token(TOKEN).build()

# --- Komut tanımları ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif ve çalışıyor!")

application.add_handler(CommandHandler("start", start))

@app.route('/')
def home():
    return "Bot is running", 200


@app.route('/webhook', methods=['POST'])
async def webhook():
    """Telegram'dan gelen güncellemeleri işleyen asenkron endpoint."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    if not application.initialized:
        await application.initialize()
    await application.process_update(update)
    return "OK", 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
