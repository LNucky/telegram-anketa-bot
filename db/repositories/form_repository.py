from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.repositories.base import BaseRepository
from db.models import Form


class FormRepository(BaseRepository[Form]):
    """Репозиторий для работы с моделью Form."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Form)

    async def get_by_id_with_author(self, form_id: int) -> Optional[Form]:
        """Получить активную форму по ID с загруженным автором."""
        result = await self.session.execute(
            select(Form)
            .options(selectinload(Form.author))
            .where(Form.id == form_id, Form.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_all_by_author_id(self, author_id: int) -> list[Form]:
        """Получить все активные формы пользователя по его ID."""
        result = await self.session.execute(
            select(Form).where(Form.author_id == author_id, Form.is_active == True)
        )
        return list(result.scalars().all())

    async def get_all_with_authors(self) -> list[Form]:
        """Получить все активные формы с загруженными авторами."""
        result = await self.session.execute(
            select(Form)
            .options(selectinload(Form.author))
            .where(Form.is_active == True)
        )
        return list(result.scalars().all())

