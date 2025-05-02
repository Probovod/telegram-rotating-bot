
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_HOST = os.getenv('RENDER_EXTERNAL_URL') or os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', default=8000))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

def get_main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔥 Консультация", url="https://t.me/m/gelSYGDAYzg6"),
        InlineKeyboardButton("📦 Получить архив", callback_data="archive"),
        InlineKeyboardButton("📊 Таблица оцифровки", url="https://t.me/m/IwCldIQEZWIy")
    )
    return kb

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} запустил бота")
    await message.answer(
        "👋 Привет, меня зовут Александр.\n"
        "Занимаюсь Wildberries более двух лет. Выбери, что тебе интересно:",
        reply_markup=get_main_menu()
    )

@dp.callback_query_handler(lambda c: c.data == 'archive')
async def send_archive(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    logging.info(f"{user_id} получил архив")
    await bot.send_message(user_id, "Сейчас отправлю полезные материалы!")
    file_path = "files/tables.zip"
    try:
        with open(file_path, "rb") as doc:
            await bot.send_document(user_id, doc)
    except Exception as e:
        logging.error(f"Ошибка отправки архива: {e}")
        await bot.send_message(user_id, "Не удалось отправить файл 😔")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(dp):
    logging.warning("Отключение вебхука...")
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
