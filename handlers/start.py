from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards.inline import get_start_keyboard
from database.db import add_user

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )

    user_name = message.from_user.full_name

    greeting_text = (
        f"Привет, {user_name}! 👋\n\n"
        "Добро пожаловать в игру <b>«Кто хочет стать миллионером?»</b> 💰\n\n"
        "Готов ли ты проверить свои знания и побороться за главный приз?\n"
        "Выбирай действие ниже и начнем!"
    )

    await message.answer(
        greeting_text,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML"
    )
