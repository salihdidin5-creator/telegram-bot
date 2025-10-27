from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

TOKEN ="8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"

app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()

# --- Komutlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif!")

application.add_handler(CommandHandler("start", start))

# --- Webhook Route ---
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    async def process():
        if not application._initialized:
            await application.initialize()
        await application.process_update(update)

    asyncio.run(process())
    return "ok", 200


@app.route('/')
def home():
    return "Bot is running!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
