import aiosqlite
import logging

QUESTIONS_DB_NAME = "questions.db"

async def init_questions_db():
    """
    Initializes the questions database and creates necessary tables if they don't exist.
    """
    try:
        async with aiosqlite.connect(QUESTIONS_DB_NAME) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    option_a TEXT,
                    option_b TEXT,
                    option_c TEXT,
                    option_d TEXT,
                    correct_option TEXT
                )
            ''')
            await db.commit()
            logging.info("Questions database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing questions database: {e}")

async def add_question(text: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_option: str):
    """
    Adds a new question to the database.
    """
    try:
        async with aiosqlite.connect(QUESTIONS_DB_NAME) as db:
            await db.execute('''
                INSERT INTO questions (text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (text, option_a, option_b, option_c, option_d, correct_option))
            await db.commit()
            logging.info("Question added successfully.")
    except Exception as e:
        logging.error(f"Error adding question: {e}")

async def get_random_questions(limit: int = 15):
    """
    Returns random questions from the database.
    """
    try:
        async with aiosqlite.connect(QUESTIONS_DB_NAME) as db:
            async with db.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT ?', (limit,)) as cursor:
                return await cursor.fetchall()
    except Exception as e:
        logging.error(f"Error getting questions: {e}")
        return []
