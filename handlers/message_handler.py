from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from handlers.states import FSMState
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories import FormRepository


router = Router()


@router.message(StateFilter(FSMState.name))
async def name_handler(message: Message, state: FSMContext):
    if message.text and 1 <= len(message.text) <= 100:
        await state.update_data(name=message.text)
        await state.set_state(FSMState.age)
        await message.answer(text="Сколько тебе лет?")
    else:
        await message.answer(text="Имя должно быть не длиннее 100 символов")

@router.message(StateFilter(FSMState.age))
async def age_handler(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if 1 <= age <= 150:
            await state.update_data(age=age)
            await state.set_state(FSMState.hobby)
            await message.answer(text="Какое у тебя хобби?")
        else:
            await message.answer(text="Введите возраст от 1 до 150")
    except Exception:
        await message.answer(text="Некорректный возраст. Ввод должен содержать число")


@router.message(StateFilter(FSMState.hobby))
async def hobby_handler(message: Message, state: FSMContext):
    if message.text and 1 <= len(message.text) <= 100:
        await state.update_data(hobby=message.text)
        await state.set_state(FSMState.color)
        await message.answer(text="Какой твой любимый цвет?")
    else:
        await message.answer(text="Ответ должен быть не длиннее 100 символов")


@router.message(StateFilter(FSMState.color))
async def color_handler(message: Message, state: FSMContext, session: AsyncSession):
    if message.text and 1 <= len(message.text) <= 100:
        await state.update_data(color=message.text)
        data = await state.get_data()
        
        # Создаем форму через репозиторий
        form_repo = FormRepository(session)
        await form_repo.create(
            author_id=data.get('author_id'),
            name=data.get('name'),
            age=data.get('age'),
            hobby=data.get('hobby'),
            color=data.get('color')
        )

        await state.clear()
        await message.answer(text="Спасибо, анкета сохранена! Чтобы заполнить еще раз — введи /start")
    else:
        await message.answer(text="Ответ должен быть не длиннее 100 символов")
        

@router.message()
async def other_messages_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await message.answer("Чтобы заполнить анкету — введи /start")