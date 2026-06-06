from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_random_questions, update_user_stats

router = Router()

class GameState(StatesGroup):
    playing = State()

def get_question_keyboard(options: list) -> InlineKeyboardMarkup:
    """Creates inline keyboard with answer options."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"A. {options[0]}", callback_data="answer_A")],
        [InlineKeyboardButton(text=f"B. {options[1]}", callback_data="answer_B")],
        [InlineKeyboardButton(text=f"C. {options[2]}", callback_data="answer_C")],
        [InlineKeyboardButton(text=f"D. {options[3]}", callback_data="answer_D")]
    ])
    return keyboard

@router.message(F.text == "🎮 Играть")
async def start_game(message: types.Message, state: FSMContext):
    """Starts the game session."""
    questions = await get_random_questions(limit=15)

    if not questions:
        await message.answer("К сожалению, в базе пока нет вопросов. Пожалуйста, зайдите позже.")
        return

    await state.set_state(GameState.playing)
    await state.update_data(questions=questions, current_index=0, win_amount=0)

    await send_next_question(message, state)

async def send_next_question(message: types.Message | types.CallbackQuery, state: FSMContext):
    """Sends the next question."""
    data = await state.get_data()
    questions = data.get("questions")
    current_index = data.get("current_index")

    if current_index >= len(questions):
        # User answered all questions correctly
        win_amount = 1000000  # simplified max win
        await update_user_stats(message.from_user.id, win_amount)
        await state.clear()

        text = "🎉 Поздравляем! Вы ответили на все вопросы и выиграли <b>1,000,000</b>!"
        if isinstance(message, types.CallbackQuery):
            await message.message.answer(text, parse_mode="HTML")
            await message.answer()
        else:
            await message.answer(text, parse_mode="HTML")
        return

    question = questions[current_index]
    # structure: (id, text, option_a, option_b, option_c, option_d, correct_option)
    q_text = question[1]
    options = [question[2], question[3], question[4], question[5]]

    msg_text = f"<b>Вопрос {current_index + 1}:</b>\n{q_text}"
    keyboard = get_question_keyboard(options)

    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(msg_text, reply_markup=keyboard, parse_mode="HTML")
        await message.answer()
    else:
        await message.answer(msg_text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(GameState.playing, F.data.startswith("answer_"))
async def process_answer(callback: types.CallbackQuery, state: FSMContext):
    """Processes the user's answer."""
    selected_option = callback.data.split("_")[1] # A, B, C, or D

    data = await state.get_data()
    questions = data.get("questions")
    current_index = data.get("current_index")

    question = questions[current_index]
    correct_option = question[6]

    if selected_option == correct_option:
        # Correct answer
        new_index = current_index + 1
        # Calculate win amount (simplified logic)
        win_amount = new_index * 1000

        await state.update_data(current_index=new_index, win_amount=win_amount)
        await send_next_question(callback, state)
    else:
        # Wrong answer
        win_amount = data.get("win_amount", 0)
        await update_user_stats(callback.from_user.id, win_amount)
        await state.clear()

        await callback.message.edit_text(
            f"❌ Неверно! Правильный ответ: <b>{correct_option}</b>.\n"
            f"Игра окончена. Ваш выигрыш: <b>{win_amount}</b>.",
            parse_mode="HTML"
        )
        await callback.answer()
