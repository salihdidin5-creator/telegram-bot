from flask import Flask, request
from telegram import Bot, Update
from telegram.error import TelegramError

import os

# -------------------------
# 1. Telegram bilgileri
# -------------------------
TOKEN = "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk"  # BotFather'dan aldığınız token
bot = Bot(token=TOKEN)

app = Flask(__name__)

# -------------------------
# 2. Mesaj gönderme fonksiyonu
# -------------------------
def send_message(chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        print(f"TelegramError: {e}")

# -------------------------
# 3. Webhook endpoint
# -------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.effective_chat.id
    message_text = update.message.text

    # Basit cevap
    send_message(chat_id, f"Mesajınızı aldım: {message_text}")
    return "ok"

# -------------------------
# 4. Test endpoint (opsiyonel)
# -------------------------
@app.route("/")
def index():
    return "Bot çalışıyor ✅"

# -------------------------
# 5. Çalıştırma
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
