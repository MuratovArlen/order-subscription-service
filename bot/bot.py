import logging
import os
import re
import psycopg2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, отправьте свой номер телефона (в формате +996700123456)")

async def save_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    telegram_id = update.effective_user.id

    # Проверка формата номера
    if not re.match(r'^\+996\d{9}$', phone):
        await update.message.reply_text("Неверный формат номера. Пример: +996700123456")
        return

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, telegram_id FROM accounts_customuser WHERE phone = %s", (phone,))
        user = cur.fetchone()

        if not user:
            await update.message.reply_text("Пользователь с таким номером не найден.")
            return

        user_id, existing_telegram_id = user

        if existing_telegram_id:
            await update.message.reply_text("Вы уже зарегистрированы в системе!")
            return

        cur.execute("UPDATE accounts_customuser SET telegram_id = %s WHERE id = %s", (telegram_id, user_id))
        conn.commit()

        await update.message.reply_text("Вы успешно зарегистрированы в системе!")

    except Exception as e:
        logger.error(f"Ошибка при работе с базой: {e}")
        await update.message.reply_text("Произошла ошибка при подключении к базе.")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_phone))

    logger.info("Бот запущен...")
    app.run_polling()
