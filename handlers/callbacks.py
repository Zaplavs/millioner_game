from aiogram import Router, F, types
from database import get_user_profile

router = Router()

@router.message(F.text == "📜 Правила")
async def rules_handler(message: types.Message) -> None:
    """
    Handler for the 'Rules' button in ReplyKeyboardMarkup
    """
    rules_text = (
        "📜 <b>Правила игры:</b>\n\n"
        "1. Вам будет предложено 15 вопросов с 4 вариантами ответов.\n"
        "2. У вас есть 3 подсказки: 50:50, Звонок другу и Помощь зала.\n"
        "3. В игре есть две несгораемые суммы.\n"
        "4. Чтобы выиграть миллион, нужно ответить на все 15 вопросов правильно!\n\n"
        "Удачи!"
    )

    await message.answer(rules_text, parse_mode="HTML")


@router.message(F.text == "🏆 Таблица лидеров")
async def leaderboard_handler(message: types.Message) -> None:
    """
    Handler for the 'Leaderboard' button in ReplyKeyboardMarkup
    """
    await message.answer("Раздел в разработке")


@router.message(F.text == "👤 Профиль")
async def profile_handler(message: types.Message) -> None:
    """
    Handler for the 'Profile' button in ReplyKeyboardMarkup
    """
    user_data = await get_user_profile(message.from_user.id)
    if user_data:
        full_name, games_played, max_win = user_data
        profile_text = (
            f"👤 <b>Профиль:</b> {full_name}\n"
            f"🎮 <b>Сыграно игр:</b> {games_played}\n"
            f"💰 <b>Максимальный выигрыш:</b> {max_win}"
        )
    else:
        profile_text = "Профиль не найден. Пожалуйста, введите /start"

    await message.answer(profile_text, parse_mode="HTML")
