from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Creates the main reply keyboard menu."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Играть")],
            [KeyboardButton(text="📜 Правила"), KeyboardButton(text="🏆 Таблица лидеров")],
            [KeyboardButton(text="👤 Профиль")]
        ],
        resize_keyboard=True
    )
    return keyboard
