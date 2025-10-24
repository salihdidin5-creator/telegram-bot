from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging
import os

# Telegram bot bilgileri
TOKEN = "8199299680:AAG7qiEUn8x8Cq64KXB38O7_uYvWgyvcQIk"
CHAT_ID = "1211267625"

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Loglama
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dispatcher oluştur
dispatcher = Dispatcher(bot, None, workers=0)

# --- KOMUTLAR ---

def start(update, context):
    # Butonlu menü oluştur
    keyboard = [
        ["🆘 Yardım", "ℹ️ Hakkında"],
        ["📞 İletişim", "🎲 Rastgele Mesaj"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "👋 Merhaba! Ben senin botunum.\nBir seçenek seç veya mesaj yaz:",
        reply_markup=reply_markup
    )

def help_command(update, context):
    update.message.reply_text("📋 Komutlar:\n/start - Başlat\n/help - Yardım al")

# --- MESAJLAR ---

def handle_message(update, context):
    text = update.message.text.lower()

    if "yardım" in text:
        reply = "🆘 Yardım menüsündesin. Sorun varsa bana yazabilirsin."
    elif "hakkında" in text:
        reply = "ℹ️ Ben Python ve Flask ile yapılmış bir Telegram botuyum!"
    elif "iletişim" in text:
        reply = "📞 Beni yapan kişiyle iletişime geçmek için: @username (örnek)"
    elif "rastgele" in text:
        import random
        cevaplar = ["Bugün harika görünüyorsun 😎", "Bir kahve molası zamanı ☕", "Şans seninle 🍀"]
        reply = random.choice(cevaplar)
    elif "merhaba" in text or "selam" in text:
        reply = "👋 Merhaba! Nasılsın?"
    elif "nasılsın" in text:
        reply = "🤖 Ben çok iyiyim, sen nasılsın?"
    elif "görüşürüz" in text or "bye" in text:
        reply = "👋 Görüşmek üzere!"
    elif "teşekkür" in text:
        reply = "Rica ederim 😊"
    else:
        reply = f"Mesajını aldım: {text}"

    update.message.reply_text(reply)

# Dispatcher’a handler’ları ekle
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# --- WEBHOOK ---

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def home():
    return "Bot aktif 🚀"

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), debug=True)
