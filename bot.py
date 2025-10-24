from flask import Flask, request
from telegram import Bot, Update
from telegram.error import TelegramError

# 🔐 Telegram bilgileri
TOKEN = "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk"

# 🔧 Bot ve Flask uygulaması
bot = Bot(token=TOKEN)
app = Flask(__name__)

# 🔹 Ana sayfa kontrolü
@app.route("/")
def index():
    return "Bot çalışıyor ✅"

# 🔹 Telegram webhook endpoint'i
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        # Telegram'dan gelen güncellemeyi al
        update = Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id if update.effective_chat else None
        message_text = update.message.text if update.message else ""

        # Gelen mesajı kontrol et
        if chat_id:
            if message_text.lower() == "/start":
                bot.send_message(chat_id=chat_id, text="Merhaba! Bot aktif ✅")
            else:
                bot.send_message(chat_id=chat_id, text=f"Gönderdiğin mesaj: {message_text}")

        return {"ok": True}

    except TelegramError as e:
        print("Telegram hatası:", e)
        return {"ok": False, "error": str(e)}, 500
    except Exception as e:
        print("Genel hata:", e)
        return {"ok": False, "error": str(e)}, 500

# 🔹 Uygulamayı başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
