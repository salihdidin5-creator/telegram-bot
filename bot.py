from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import asyncio
import logging

# --------------------------------------------------
# 🔹 Flask uygulaması
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# 🔹 Telegram Bot Token (Render ortam değişkeni olarak eklenmeli)
# --------------------------------------------------
TOKEN = os.getenv("8199299680:AAGUONCVNwZVhLtZb1Eq-8OIay7SsBN_U5w")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# --------------------------------------------------
# 🔹 Logging ayarları
# --------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --------------------------------------------------
# 🔹 Bot komutları
# --------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Merhaba! Bot başarıyla çalışıyor.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Komutlar:\n/start - Botu başlatır\n/help - Yardım mesajı gösterir")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kullanıcının yazdığını geri yollar
    await update.message.reply_text(update.message.text)

# --------------------------------------------------
# 🔹 Application (Dispatcher yerine)
# --------------------------------------------------
application = ApplicationBuilder().token(TOKEN).build()

# Komut ve mesaj handler’ları ekleniyor
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --------------------------------------------------
# 🔹 Flask route'ları
# --------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return "🤖 Bot is running!", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Telegram'dan gelen güncellemeleri işler"""
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "ok", 200

# --------------------------------------------------
# 🔹 Uygulama başlatma (Render için)
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
