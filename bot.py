import logging
import os
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from fact_fetcher import fetch_random_fact, fetch_fact_by_topic # Импортируем функции из файла fact_fetcher.py

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Загрузка токена из переменной окружения (или жестко заданный токен)
TOKEN = "7567918886:AAHrbIbuUMpyc0NO-HgN6vbFJPqIEmY6k2k" # Здесь ваш токен
if not TOKEN:
    raise ValueError("7567918886:AAHrbIbuUMpyc0NO-HgN6vbFJPqIEmY6k2k environment variable not set.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение приветствия при старте."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я могу рассказать тебе интересный факт или факт по заданной теме. Напиши /help для списка команд.",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение со списком команд."""
    await update.message.reply_text("/random - случайный факт\n/topic [тема] - факт на заданную тему")

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет случайный факт."""
    try:
        fact = fetch_random_fact()
        await update.message.reply_text(fact)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

async def topic_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет факт на заданную тему."""
    topic = ' '.join(context.args)
    if not topic:
        await update.message.reply_text("Укажите тему!")
        return
    try:
        fact = fetch_fact_by_topic(topic)
        await update.message.reply_text(fact)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Извини, я не понимаю эту команду.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавление обработчиков команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("random", random_fact))
    application.add_handler(CommandHandler("topic", topic_fact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    # Запуск бота
    application.run_polling()