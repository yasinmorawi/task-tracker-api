from typing import List, Optional 
from datetime import datetime, UTC
from sqlmodel import Field, Relationship , SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str

    tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    # Perbaikan: foreign_key disesuikan dengan __tablename__ milik user
    user_id: int = Field(foreign_key="users.id", index=True)
    owner: User = Relationship(back_populates="tasks")