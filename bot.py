import os
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.webhook import get_new_configured_app
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 10000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

menu_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("🔥 Консультация", url="https://t.me/m/gelSYGDAYzg6"),
    InlineKeyboardButton("📦 Получить материалы", callback_data="get_archive"),
    InlineKeyboardButton("📊 Таблица оцифровки", url="https://t.me/m/IwCldIQEZWIy")
)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Привет, меня зовут Александр.
Занимаюсь ВБ больше двух лет.
Выбери вариант меню, который тебе необходим.",
        reply_markup=menu_kb
    )
    logger.info(f"Пользователь {message.from_user.id} запустил бота")

@dp.callback_query_handler(lambda c: c.data == "get_archive")
async def send_archive(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
        "📦 Направляю архив с полезными материалами, например, как считать юнит-экономику или работать с ценами товаров. "
        "Скачай архив, внутри таблицы Excel. Рад помочь!")
    with open("files/tables.zip", "rb") as f:
        await bot.send_document(callback_query.from_user.id, f)
    logger.info(f"{callback_query.from_user.id} получил архив")

async def check_webhook():
    while True:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            logger.warning("🔄 Вебхук сброшен, переустанавливаю...")
            await bot.set_webhook(WEBHOOK_URL)
            logger.info(f"✅ Вебхук установлен: {WEBHOOK_URL}")
        await asyncio.sleep(600)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(check_webhook())

async def on_shutdown(app):
    logger.warning("Отключение вебхука...")
    await bot.delete_webhook()

if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
