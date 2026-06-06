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
                    full_name TEXT,
                    games_played INTEGER DEFAULT 0,
                    max_win INTEGER DEFAULT 0
                )
            ''')
            # Check if columns exist (for migration if db already exists)
            try:
                await db.execute("ALTER TABLE users ADD COLUMN games_played INTEGER DEFAULT 0")
                await db.execute("ALTER TABLE users ADD COLUMN max_win INTEGER DEFAULT 0")
            except aiosqlite.OperationalError:
                pass # Columns already exist
            await db.commit()
            logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

async def get_user_profile(telegram_id: int):
    """
    Returns user profile data.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute('SELECT full_name, games_played, max_win FROM users WHERE telegram_id = ?', (telegram_id,)) as cursor:
                return await cursor.fetchone()
    except Exception as e:
        logging.error(f"Error getting user profile: {e}")
        return None

async def update_user_stats(telegram_id: int, win_amount: int):
    """
    Updates user statistics after a game.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute('''
                UPDATE users
                SET games_played = games_played + 1,
                    max_win = CASE WHEN ? > max_win THEN ? ELSE max_win END
                WHERE telegram_id = ?
            ''', (win_amount, win_amount, telegram_id))
            await db.commit()
    except Exception as e:
        logging.error(f"Error updating user stats: {e}")

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
