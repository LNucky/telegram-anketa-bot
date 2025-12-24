from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.repositories.base import BaseRepository
from db.models import User


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с моделью User."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить активного пользователя по Telegram ID."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id, User.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_or_create_by_telegram_id(self, telegram_id: int) -> User:
        """Получить пользователя по Telegram ID или создать нового."""
        user = await self.get_by_telegram_id(telegram_id)
        if user is None:
            user = await self.create(telegram_id=telegram_id)
        return user

