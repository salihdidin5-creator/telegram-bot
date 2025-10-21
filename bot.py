import os
import logging
from flask import Flask, request
from telegram import Bot

# ---------- AYARLAR ----------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Telegram bot token
CHAT_ID = os.getenv("CHAT_ID")  # Mesaj göndereceğin grup/kanal ID
PORT = int(os.environ.get("PORT", 5000))  # Render veya Heroku için port

# ---------- LOGGING ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- TELEGRAM BOT ----------
bot = Bot(token=TELEGRAM_TOKEN)

# ---------- FLASK UYGULAMASI ----------
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot çalışıyor!"

@app.route("/send_signal", methods=["POST"])
def send_signal():
    """
    POST ile sinyal gönderebilirsin:
    {
        "message": "BTC al sinyali"
    }
    """
    data = request.get_json()
    if not data or "message" not in data:
        return {"status": "error", "message": "Mesaj gönderilmedi"}, 400

    message = data["message"]
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        logger.info(f"Sinyal gönderildi: {message}")
        return {"status": "success", "message": "Sinyal gönderildi"}, 200
    except Exception as e:
        logger.error(f"Hata: {e}")
        return {"status": "error", "message": str(e)}, 500

# ---------- ANA FONKSİYON ----------
if __name__ == "__main__":
    logger.info("Bot başlatılıyor...")
    app.run(host="0.0.0.0", port=PORT)
