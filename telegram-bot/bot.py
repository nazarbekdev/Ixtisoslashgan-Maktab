import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL")

# Bot tokeni
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botni ishga tushirish va tokenni olish"""
    token = context.args[0] if context.args else None
    if not token:
        await update.message.reply_text("Iltimos, parol tiklash jarayonini veb-saytdan boshlang.")
        return

    context.user_data['token'] = token
    await update.message.reply_text(
        "Parolni tiklash jarayonini boshlash uchun yangi parolni kiriting:")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi xabarlarini qayta ishlash"""
    if update.message.text.startswith('/'):
        return

    token = context.user_data.get('token')
    if not token:
        await update.message.reply_text("Iltimos, /start buyrug‘i bilan jarayonni boshlang.")
        return

    # Yangi parolni o‘rnatish
    new_password = update.message.text.strip()
    try:
        response = requests.post(f"{BACKEND_URL}/auth/password-reset/confirm/", json={
            'token': token,
            'new_password': new_password
        })
        if response.status_code == 200:
            await update.message.reply_text("Parol muvaffaqiyatli yangilandi! Endi tizimga kiring.")
            context.user_data.clear()
        else:
            await update.message.reply_text("Xato yuz berdi: " + response.json().get('error', 'Noma’lum xato'))
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text("Xato yuz berdi. Iltimos, qaytadan urining.")


def main() -> None:
    """Botni ishga tushirish"""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(None, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
