from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Text, Boolean, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    subtasks: Mapped[List[Subtask]] = relationship(
        back_populates="todo",
        cascade="all, delete-orphan"
    )

class Subtask(Base):
    __tablename__ = "subtasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id", ondelete="CASCADE"), index=True)

    content: Mapped[str] = mapped_column(String(255), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    todo: Mapped[Todo] = relationship(back_populates="subtasks")
