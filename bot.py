import logging
from aiogram import Bot, Dispatcher, types, executor
import os

API_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    text = (
        "👋 Привет, меня зовут Александр.\n"
        "Занимаюсь ВБ больше двух лет.\n"
        "Выбери нужный вариант меню."
    )
    await message.answer(text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
