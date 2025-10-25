from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import os

# === Telegram Bot Token ===
TOKEN = os.getenv("BOT_TOKEN", "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk")

# === Flask Uygulaması ===
app = Flask(__name__)

# === Telegram Bot Uygulaması ===
application = ApplicationBuilder().token(TOKEN).build()

# === Komutlar ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bot başarıyla çalışıyor 🚀")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Gönderdiğin mesaj: {update.message.text}")

# === Handler'ları ekle ===
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# === Telegram Webhook Endpoint ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Telegram update geldi:", data)  # Log çıktısı
        update = Update.de_json(data, application.bot)

        # Render ortamında güvenli asyncio döngüsü
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        loop.close()

    except Exception as e:
        print("Webhook hatası:", e)
        return "error", 500

    return "ok", 200

# === Basit test için ana sayfa ===
@app.route("/", methods=["GET"])
def home():
    return "Bot çalışıyor ✅", 200

# === Çalıştır ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
