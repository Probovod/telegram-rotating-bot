import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import asyncio

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔥 Консультация", url="https://t.me/m/gelSYGDAYzg6"),
        InlineKeyboardButton("📦 Получить архив", callback_data="get_archive"),
        InlineKeyboardButton("📊 Таблица оцифровки", url="https://t.me/m/IwCldIQEZWIy")
    )
    return kb

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    text = (
        "👋 Привет! Меня зовут Александр.
"
        "Занимаюсь ВБ больше двух лет.
"
        "Выбери вариант меню, который тебе необходим:"
    )
    await message.answer(text, reply_markup=main_menu())
    logging.info(f"Пользователь {message.from_user.id} запустил бота")

@dp.callback_query_handler(lambda c: c.data == "get_archive")
async def send_archive(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
        "Дорогой друг, направляю тебе архив с полезными материалами, такими как просчет юнит экономики и работа с ценами товаров. "
        "Чтобы скачать — нажми на архив. Внутри Excel-таблицы."
    )
    file_path = "files/tables.zip"
    try:
        with open(file_path, "rb") as f:
            await bot.send_document(callback_query.from_user.id, f)
        logging.info(f"{callback_query.from_user.id} получил архив")
    except Exception as e:
        logging.error(f"Ошибка при отправке архива: {e}")
        await bot.send_message(callback_query.from_user.id, "⚠️ Не удалось отправить файл.")
    await asyncio.sleep(120)
    await bot.send_message(
        callback_query.from_user.id,
        "Как тебе материалы? Давай я помогу разобраться — [напиши мне](https://t.me/m/gelSYGDAYzg6)",
        parse_mode="Markdown"
    )

async def notify_admin(dispatcher: Dispatcher):
    if ADMIN_ID:
        try:
            await bot.send_message(int(ADMIN_ID), "✅ Бот запущен.")
        except Exception as e:
            logging.error(f"Не удалось уведомить админа: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=notify_admin)
