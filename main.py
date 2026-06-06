import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, PROXY_URL
from handlers import router
from database.db import init_db

# Initialize dispatcher
dp = Dispatcher()
dp.include_router(router)


async def main() -> None:
    """
    Main function to run the bot
    """
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set. Please check your .env file.")
        sys.exit(1)

    session = None
    if PROXY_URL:
        logging.info(f"Using proxy: {PROXY_URL}")
        session = AiohttpSession(proxy=PROXY_URL)

    # Initialize Bot instance
    bot = Bot(token=BOT_TOKEN, session=session)

    # Initialize the database
    await init_db()

    # And the run events dispatching
    logging.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
