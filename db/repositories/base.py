from typing import Generic, TypeVar, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с общими методами для работы с БД."""

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить объект по ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> ModelType:
        """Создать новый объект."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Обновить существующий объект."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        """Удалить объект."""
        await self.session.delete(instance)
        await self.session.commit()

    async def get_all(self) -> list[ModelType]:
        """Получить все объекты."""
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

