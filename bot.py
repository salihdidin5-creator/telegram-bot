from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

# --- Telegram Token ---
TOKEN = os.getenv("BOT_TOKEN", "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A")

# --- Flask Uygulaması ---
app = Flask(__name__)

# --- Telegram Application ---
application = ApplicationBuilder().token(TOKEN).build()


# --- Komutlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bot başarıyla çalışıyor 🚀")


application.add_handler(CommandHandler("start", start))


# --- Webhook İşleme ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    async def process_update():
        await application.initialize()
        await application.process_update(update)
        await application.shutdown()

    # Flask içinde asyncio kullanımı
    asyncio.run(process_update())
    return "OK", 200


@app.route("/")
def home():
    return "Bot aktif ✅", 200


# --- Render'da çalıştırmak için ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
