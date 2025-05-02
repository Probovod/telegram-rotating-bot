import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{os.getenv('RENDER_EXTERNAL_URL')}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔥 Консультация", url="https://t.me/m/gelSYGDAYzg6"),
        InlineKeyboardButton("📦 Получить архив с материалами", callback_data="archive"),
        InlineKeyboardButton("📊 Получить таблицу оцифровки", url="https://t.me/m/IwCldIQEZWIy")
    )
    return kb

@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    await message.answer(
        "👋 Привет, меня зовут Александр.
"
        "Занимаюсь ВБ больше двух лет.
"
        "Выбери вариант меню, который тебе необходим:",
        reply_markup=main_menu()
    )
    logging.info(f"Пользователь {message.from_user.id} запустил бота")

@dp.callback_query_handler(lambda c: c.data == "archive")
async def handle_archive(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
        "Дорогой друг, направляю тебе архив с полезными материалами. Нажми на файл, чтобы скачать."
    )
    file_path = "files/tables.zip"
    try:
        with open(file_path, "rb") as f:
            await bot.send_document(callback_query.from_user.id, f)
        logging.info(f"{callback_query.from_user.id} получил архив")
    except Exception as e:
        await bot.send_message(callback_query.from_user.id, "⚠️ Не удалось отправить файл.")
        logging.error(f"Ошибка при отправке архива: {e}")

    await asyncio.sleep(120)
    await bot.send_message(
        callback_query.from_user.id,
        "Как тебе материалы? Давай я помогу разобраться, [напиши мне](https://t.me/m/gelSYGDAYzg6)",
        parse_mode="Markdown"
    )
