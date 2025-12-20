from sqlalchemy import BigInteger, Integer, Text, ForeignKey, Column
from sqlalchemy.orm import relationship
from db.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, unique=True, nullable=False)

    forms = relationship("Form", back_populates="author", cascade="all, delete-orphan")


class Form(BaseModel):
    __tablename__ = "forms"

    author_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text)
    age = Column(Integer)
    hobby = Column(Text)
    color = Column(Text)

    author = relationship("User", back_populates="forms")
