from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from typing import Optional
from app.enums.generation_status import GenerationStatus


class Base(DeclarativeBase):
    pass


class Generation(Base):
    __tablename__ = "generations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[GenerationStatus] = mapped_column(String)
    prompt: Mapped[str] = mapped_column(String)
    model_name: Mapped[str] = mapped_column(String)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
