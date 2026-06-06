from aiogram import Router, F, types

router = Router()

@router.callback_query(F.data == "rules")
async def rules_handler(callback: types.CallbackQuery) -> None:
    """
    Handler for the 'Rules' button
    """
    rules_text = (
        "📜 <b>Правила игры:</b>\n\n"
        "1. Вам будет предложено 15 вопросов с 4 вариантами ответов.\n"
        "2. У вас есть 3 подсказки: 50:50, Звонок другу и Помощь зала.\n"
        "3. В игре есть две несгораемые суммы.\n"
        "4. Чтобы выиграть миллион, нужно ответить на все 15 вопросов правильно!\n\n"
        "Удачи!"
    )

    await callback.message.answer(rules_text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "leaderboard")
async def leaderboard_handler(callback: types.CallbackQuery) -> None:
    """
    Handler for the 'Leaderboard' button
    """
    await callback.answer("Раздел в разработке", show_alert=True)


@router.callback_query(F.data == "play")
async def play_handler(callback: types.CallbackQuery) -> None:
    """
    Placeholder handler for the 'Play' button
    """
    await callback.answer("Игра скоро начнется!", show_alert=True)
