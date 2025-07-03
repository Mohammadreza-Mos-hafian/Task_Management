from __future__ import annotations

from typing import List, Optional, Type

from flask_login import UserMixin

from sqlalchemy import (
    Boolean, String, DateTime, Identity, Integer,
    PrimaryKeyConstraint, UniqueConstraint,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from app.database import Base, engine

from datetime import datetime


class User(Base, UserMixin):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id: Mapped[int] = mapped_column(Integer,
                                    Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647,
                                             cycle=False, cache=1), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'),
                                                 onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='user')

    @staticmethod
    def load_user(user_id: str) -> Type[User] | None:
        with Session(engine) as session:
            user = session.get(User, int(user_id))

            if user:
                return user

        return None
