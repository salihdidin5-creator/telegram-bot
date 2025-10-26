from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk"

app = Flask(__name__)

# --- Telegram Komutları ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Merhaba! Bot başarıyla çalışıyor.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yardım menüsüne hoş geldin!")

# --- Flask rotası (webhook) ---
@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "ok", 200

# --- Bot uygulaması ---
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot

# Komutları ekle
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Render için ana sayfa kontrolü
@app.route("/")
def home():
    return "Bot aktif!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
