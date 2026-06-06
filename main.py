import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router

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

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN)

    # And the run events dispatching
    logging.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
