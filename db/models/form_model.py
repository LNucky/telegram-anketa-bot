from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base_model import BaseModel

if TYPE_CHECKING:
    from db.models.user_model import User


class Form(BaseModel):
    __tablename__ = "forms"

    author_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(Text)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    hobby: Mapped[Optional[str]] = mapped_column(Text)
    color: Mapped[Optional[str]] = mapped_column(Text)

    author: Mapped["User"] = relationship(back_populates="forms")

