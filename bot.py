from flask import Flask, request
from telegram import Bot
from telegram.error import TelegramError

# Telegram bilgileri
TOKEN = "8199299680:AAGUONCVNwZVhLtZb1Eq-8OIay7SsBN_U5w"
CHAT_ID = "1211267625"

bot = Bot(token=TOKEN)
app = Flask(__name__)

def send_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        print("Mesaj gönderildi:", text)
    except TelegramError as e:
        print("Hata oluştu:", e)

@app.route("/")
def index():
    return "Bot çalışıyor ✅"

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    mesaj = data.get("message", "Varsayılan mesaj")
    send_message(mesaj)
    return {"status": "success", "message_sent": mesaj}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
