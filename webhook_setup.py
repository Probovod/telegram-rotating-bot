import os
import asyncio
import logging
from aiohttp import web
from bot import bot, dp, WEBHOOK_PATH, WEBHOOK_URL
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

async def on_startup(app):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        logging.info(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.info("Выключение...")
    await bot.session.close()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
