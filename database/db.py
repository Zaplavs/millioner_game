import aiosqlite
import logging

DB_NAME = "bot_database.db"

async def init_db():
    """
    Initializes the database and creates necessary tables if they don't exist.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT
                )
            ''')
            await db.commit()
            logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

async def add_user(telegram_id: int, username: str, full_name: str):
    """
    Adds a new user to the database if they don't already exist.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute('''
                INSERT OR IGNORE INTO users (telegram_id, username, full_name)
                VALUES (?, ?, ?)
            ''', (telegram_id, username, full_name))
            await db.commit()
            logging.info(f"User {telegram_id} added/checked in database.")
    except Exception as e:
        logging.error(f"Error adding user to database: {e}")
