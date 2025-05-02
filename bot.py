import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import asyncio

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Логирование
log_handler = RotatingFileHandler("bot.log", maxBytes=1024*1024, backupCount=5, encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler, logging.StreamHandler()]
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📦 Файлы", callback_data="menu:files"),
        InlineKeyboardButton("📊 Таблицы", callback_data="menu:tables"),
        InlineKeyboardButton("🌐 Полезные ссылки", callback_data="menu:links"),
        InlineKeyboardButton("🔥 Консультация", url="https://t.me/m/gelSYGDAYzg6")
    )
    return kb

def files_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📥 Скачать архив с таблицами", callback_data="action:send_archive"),
        InlineKeyboardButton("↩️ Назад", callback_data="menu:main")
    )
    return kb

def tables_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📊 Открыть таблицу оцифровки", url="https://t.me/m/IwCldIQEZWIy"),
        InlineKeyboardButton("↩️ Назад", callback_data="menu:main")
    )
    return kb

def links_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🌍 Wildberries Seller", url="https://seller.wildberries.ru/"),
        InlineKeyboardButton("📘 WB Guru", url="https://wb.guru"),
        InlineKeyboardButton("↩️ Назад", callback_data="menu:main")
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

@dp.callback_query_handler(lambda c: c.data.startswith("menu:"))
async def handle_menu(callback_query: types.CallbackQuery):
    data = callback_query.data.split(":")[1]
    if data == "main":
        await callback_query.message.edit_text("📋 Главное меню:", reply_markup=main_menu())
    elif data == "files":
        await callback_query.message.edit_text("📦 Файлы:", reply_markup=files_menu())
    elif data == "tables":
        await callback_query.message.edit_text("📊 Таблицы:", reply_markup=tables_menu())
    elif data == "links":
        await callback_query.message.edit_text("🌐 Полезные ссылки:", reply_markup=links_menu())

@dp.callback_query_handler(lambda c: c.data.startswith("action:send_archive"))
async def send_archive(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
        "Дорогой друг, направляю тебе архив с очень полезными материалами, например, как просчет юнит экономики или работа с ценами товаров. "
        "Для того, чтобы скачать, нажми на архив. В нем будет Excel формата таблицы. Был рад тебе помочь."
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

async def notify_admin_on_startup(dispatcher: Dispatcher):
    if ADMIN_ID:
        try:
            await bot.send_message(int(ADMIN_ID), "✅ Бот запущен. Главное меню готово.")
        except Exception as e:
            logging.error(f"Ошибка при уведомлении: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=notify_admin_on_startup)
