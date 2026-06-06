from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import add_question

router = Router()

class AdminQuestionState(StatesGroup):
    waiting_for_text = State()
    waiting_for_option_a = State()
    waiting_for_option_b = State()
    waiting_for_option_c = State()
    waiting_for_option_d = State()
    waiting_for_correct_option = State()


@router.message(Command("admin"))
async def admin_start(message: types.Message, state: FSMContext):
    """Starts the process of adding a new question."""
    # Note: In a real bot, you'd want to check if the user is an admin here.
    # For this example, we'll allow anyone who knows the /admin command.
    await message.answer("🛠 <b>Режим администратора</b>\n\nВведите текст нового вопроса:", parse_mode="HTML")
    await state.set_state(AdminQuestionState.waiting_for_text)


@router.message(AdminQuestionState.waiting_for_text)
async def process_question_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Введите вариант ответа A:")
    await state.set_state(AdminQuestionState.waiting_for_option_a)


@router.message(AdminQuestionState.waiting_for_option_a)
async def process_option_a(message: types.Message, state: FSMContext):
    await state.update_data(option_a=message.text)
    await message.answer("Введите вариант ответа B:")
    await state.set_state(AdminQuestionState.waiting_for_option_b)


@router.message(AdminQuestionState.waiting_for_option_b)
async def process_option_b(message: types.Message, state: FSMContext):
    await state.update_data(option_b=message.text)
    await message.answer("Введите вариант ответа C:")
    await state.set_state(AdminQuestionState.waiting_for_option_c)


@router.message(AdminQuestionState.waiting_for_option_c)
async def process_option_c(message: types.Message, state: FSMContext):
    await state.update_data(option_c=message.text)
    await message.answer("Введите вариант ответа D:")
    await state.set_state(AdminQuestionState.waiting_for_option_d)


@router.message(AdminQuestionState.waiting_for_option_d)
async def process_option_d(message: types.Message, state: FSMContext):
    await state.update_data(option_d=message.text)
    await message.answer("Укажите правильный вариант ответа (A, B, C или D):")
    await state.set_state(AdminQuestionState.waiting_for_correct_option)


@router.message(AdminQuestionState.waiting_for_correct_option)
async def process_correct_option(message: types.Message, state: FSMContext):
    correct_option = message.text.strip().upper()
    if correct_option not in ["A", "B", "C", "D"]:
        await message.answer("Пожалуйста, введите только одну букву: A, B, C или D.")
        return

    user_data = await state.get_data()

    await add_question(
        text=user_data['text'],
        option_a=user_data['option_a'],
        option_b=user_data['option_b'],
        option_c=user_data['option_c'],
        option_d=user_data['option_d'],
        correct_option=correct_option
    )

    await message.answer("✅ Вопрос успешно добавлен в базу данных!")
    await state.clear()
