from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base_model import BaseModel

if TYPE_CHECKING:
    from db.models.form_model import Form


class User(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    forms: Mapped[list["Form"]] = relationship(back_populates="author", cascade="all, delete-orphan")

