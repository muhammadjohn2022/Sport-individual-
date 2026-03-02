import logging
import threading
import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# Kalitlarni Render'dan xavfsiz olish
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask('')
@app.route('/')
def home(): return "Bot uyg'oq!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # 2026-yil uchun barqaror model
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=user_text,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {str(e)}")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # drop_pending_updates=True konfliktlarni va tiqilib qolgan eski xabarlarni tozalaydi
    application.run_polling(drop_pending_updates=True)
