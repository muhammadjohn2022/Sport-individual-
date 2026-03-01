import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai
import os

# Kalitlar
TELEGRAM_TOKEN = '8672369792:AAFO80iJTSZZBBinKIoy0E-Ll4_A-vDn6I4'
GEMINI_API_KEY = 'AIzaSyCYgatMgekG4EQdtpbeBvq2TiF-_7EUb7c'

# Gemini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Loglarni aniq chiqarish uchun sozlama
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Veb-server (Render uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Bot xabarlarni qabul qilganda ishlaydigan qism
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        # XATONI TO'G'RIDAN-TO'G'RI TELEGRAMGA YUBORAMIZ!
        xato_matni = f"GEMINI XATOSI: {str(e)}"
        await update.message.reply_text(xato_matni)
        logging.error(xato_matni)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot va Veb-server ishga tushdi...", flush=True)
    application.run_polling()
