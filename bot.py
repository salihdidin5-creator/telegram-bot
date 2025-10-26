from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

# --- Telegram Token ---
TOKEN = "8240614382:AAFKTK10nOqbDp6SwJPMRrSDQxA5Hok2a7A"

# --- Flask Uygulaması ---
app = Flask(__name__)

# --- Telegram Application ---
application = Application.builder().token(TOKEN).build()
bot = application.bot

# --- Komutlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Merhaba! Bot çalışıyor ve webhook bağlantısı aktif.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ /start komutu ile botu test edebilirsin.")

# --- Handler'ları ekle ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# --- Webhook endpoint ---
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        asyncio.run(application.process_update(update))
    except Exception as e:
        print(f"❌ Webhook hatası: {e}")
        return "error", 500
    return "ok", 200

# --- Ana sayfa (kontrol için) ---
@app.route("/")
def home():
    return "🚀 Telegram Bot aktif (Flask + Render)", 200

# --- Render ortamında çalıştır ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
