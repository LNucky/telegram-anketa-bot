from aiogram.types import Message, FSInputFile
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from handlers.states import FSMState
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories import UserRepository, FormRepository
from openpyxl import Workbook
import tempfile
import os

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext, session: AsyncSession):
    # Получаем или создаем пользователя
    user_repo = UserRepository(session)
    user = await user_repo.get_or_create_by_telegram_id(message.from_user.id)

    if await state.get_state():
        await message.answer("Давай заполним анкету заново. Как тебя зовут?")
        
    else:
        await message.answer(text="Привет! Давай заполним анкету. Как тебя зовут?")
    await state.set_state(FSMState.name)
    await state.update_data(author_id=user.id)


@router.message(Command("admin"))
async def admin_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    if message.from_user.id in settings.admin_ids:
        # Получаем все анкеты с авторами из БД
        form_repo = FormRepository(session)
        forms = await form_repo.get_all_with_authors()
        
        if not forms:
            await message.answer("Анкет пока нет в базе данных")
            return
        
        # Создаем словарь для быстрого доступа к telegram_id авторов
        users_dict = {form.author.id: form.author.telegram_id for form in forms if form.author}
        
        # Создаем Excel файл
        wb = Workbook()
        ws = wb.active
        ws.title = "Анкеты"
        
        # Заголовки
        headers = ["ID", "Telegram ID автора", "Имя", "Возраст", "Хобби", "Цвет", "Дата создания"]
        ws.append(headers)
        
        # Заполняем данными
        for form in forms:
            telegram_id = users_dict.get(form.author_id, "N/A")
            
            ws.append([
                form.id,
                telegram_id,
                form.name or "",
                form.age or "",
                form.hobby or "",
                form.color or "",
                form.created_at.strftime("%Y-%m-%d %H:%M:%S") if form.created_at else ""
            ])
        
        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            wb.save(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        # Отправляем файл
        document = FSInputFile(tmp_file_path, filename="ankety.xlsx")
        await message.answer_document(document, caption="⬆️ Файл со всеми анкетами ⬆️")
        
        # Удаляем временный файл
        os.unlink(tmp_file_path)
    else:
        await message.answer(text="У вас нет доступа к этой команде")