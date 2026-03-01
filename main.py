import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai
import os

# 1. SOZLAMALAR (Sizning kalitlaringiz)
TELEGRAM_TOKEN = '8672369792:AAFO80iJTSZZBBinKIoy0E-Ll4_A-vDn6I4'
GEMINI_API_KEY = 'AIzaSyCYgatMgekG4EQdtpbeBvq2TiF-_7EUb7c'

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Loglar
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. RENDER UCHUN KICHIK VEB-SERVER (Flask)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    # Render avtomatik beradigan PORT-ni olamiz
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 3. TELEGRAM BOT FUNKSIYASI
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")
        print(f"Xato: {e}")

# 4. ASOSIY ISHGA TUSHIRISH
if __name__ == '__main__':
    # Flask-ni alohida "oqim"da (thread) boshlaymiz
    threading.Thread(target=run_flask).start()
    
    # Telegram botni boshlaymiz
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot va Veb-server ishga tushdi...")
    application.run_polling()

