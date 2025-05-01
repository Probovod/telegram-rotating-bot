
import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Настройка логгирования с ротацией
log_handler = RotatingFileHandler(
    filename="bot.log",
    maxBytes=1024 * 1024,  # 1 МБ
    backupCount=5,         # Хранить до 5 архивов
    encoding="utf-8"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler, logging.StreamHandler()]
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Привет! Меня зовут Александр. Хотел бы познакомиться с тобой подробнее.\n\n"
        "Я являюсь менеджером и занимаюсь Валбрисом больше двух лет.\n"
        "Хочу поделиться с тобой полезными материалами — совершенно бесплатно!"
    )
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Получить файл с таблицами", callback_data='get_files'),
        InlineKeyboardButton("Получить таблицу оцифровки", callback_data='get_table'),
        InlineKeyboardButton("Получить полезные ссылки", callback_data='get_links'),
        InlineKeyboardButton("Записаться на консультацию", url='https://t.me/alex_valberis')
    )
    await message.answer(welcome_text, reply_markup=keyboard)
    logging.info(f"/start от пользователя {message.from_user.id}")

@dp.callback_query_handler(lambda c: c.data == 'get_files')
async def send_files(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Файл с таблицами сейчас недоступен на облаке. Напишите мне лично.")
    logging.info(f"{callback_query.from_user.id} запросил файл с таблицами")

@dp.callback_query_handler(lambda c: c.data == 'get_table')
async def send_table(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Таблица оцифровки сейчас недоступна. Напишите мне лично.")
    logging.info(f"{callback_query.from_user.id} запросил таблицу оцифровки")

@dp.callback_query_handler(lambda c: c.data == 'get_links')
async def send_links(callback_query: types.CallbackQuery):
    text = (
        "Вот несколько полезных ссылок:\n"
        "1. [Wildberries Seller](https://seller.wildberries.ru/)\n"
        "2. [WB Guru](https://wb.guru)"
    )
    await bot.send_message(callback_query.from_user.id, text, parse_mode="Markdown")
    logging.info(f"{callback_query.from_user.id} запросил полезные ссылки")

async def notify_admin_on_startup(dispatcher: Dispatcher):
    if ADMIN_ID:
        try:
            await bot.send_message(int(ADMIN_ID), "✅ Бот успешно запущен на Render!")
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=notify_admin_on_startup)
