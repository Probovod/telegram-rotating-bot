import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import asyncio

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Логирование с ротацией
log_handler = RotatingFileHandler("bot.log", maxBytes=1024*1024, backupCount=5, encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler, logging.StreamHandler()]
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📦 Получить файл с таблицами", callback_data="files"),
        InlineKeyboardButton("📊 Таблица оцифровки", url="https://t.me/m/IwCldIQEZWIy"),
        InlineKeyboardButton("🌐 Полезные ссылки", callback_data="links"),
        InlineKeyboardButton("🔥 Консультация", url="https://t.me/m/gelSYGDAYzg6")
    )
    return kb

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    text = (
        "👋 Привет! Меня зовут Александр.\n"
        "Я менеджер WB с опытом более двух лет.\n"
        "Готов бесплатно поделиться полезными материалами."
    )
    await message.answer(text, reply_markup=main_menu())
    logging.info(f"Старт: {message.from_user.id}")

@dp.callback_query_handler(lambda c: c.data == "files")
async def send_archive(callback_query: types.CallbackQuery):
    file_path = "files/tables.zip"
    try:
        with open(file_path, "rb") as f:
            await bot.send_document(callback_query.from_user.id, f)
        logging.info(f"{callback_query.from_user.id} получил архив")
    except Exception as e:
        await bot.send_message(callback_query.from_user.id, "⚠️ Не удалось отправить файл.")
        logging.error(f"Ошибка при отправке архива: {e}")
    await bot.send_message(callback_query.from_user.id, "🔙 Вернуться в меню", reply_markup=main_menu())
    await asyncio.sleep(30)
    await bot.send_message(
        callback_query.from_user.id,
        "Как тебе материалы? Давай я помогу разобраться, [напиши мне](https://t.me/m/gelSYGDAYzg6)",
        parse_mode="Markdown"
    )

@dp.callback_query_handler(lambda c: c.data == "links")
async def send_links(callback_query: types.CallbackQuery):
    text = (
        "🔗 Полезные ссылки:\n"
        "• [Wildberries Seller](https://seller.wildberries.ru/)\n"
        "• [WB Guru](https://wb.guru)"
    )
    await bot.send_message(callback_query.from_user.id, text, parse_mode="Markdown")
    logging.info(f"{callback_query.from_user.id} запросил ссылки")
    await bot.send_message(callback_query.from_user.id, "🔙 Вернуться в меню", reply_markup=main_menu())
    await asyncio.sleep(30)
    await bot.send_message(
        callback_query.from_user.id,
        "Как тебе материалы? Давай я помогу разобраться, [напиши мне](https://t.me/m/gelSYGDAYzg6)",
        parse_mode="Markdown"
    )

async def notify_admin_on_startup(dispatcher: Dispatcher):
    if ADMIN_ID:
        try:
            await bot.send_message(int(ADMIN_ID), "✅ Бот запущен. Главное меню готово.")
        except Exception as e:
            logging.error(f"Ошибка при уведомлении: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=notify_admin_on_startup)
