from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os, asyncio

TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"

app = Flask(__name__)

# --- Telegram komutları ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Merhaba! Bot başarıyla çalışıyor.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yardım menüsüne hoş geldin!")

# --- Telegram uygulaması ---
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# --- Webhook rotası (event loop güvenli) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        loop.create_task(application.process_update(update))
    else:
        loop.run_until_complete(application.process_update(update))

    return "ok", 200

# --- Ana sayfa ---
@app.route("/")
def home():
    return "Bot aktif!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
