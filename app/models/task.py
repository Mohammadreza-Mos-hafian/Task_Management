from __future__ import annotations

from typing import List, Optional

from sqlalchemy import (
    BigInteger, Boolean, Date, DateTime, Identity, Integer, SmallInteger, String, Text,
    PrimaryKeyConstraint, ForeignKeyConstraint,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE',
                             name='tasks_user_id_fkey'),
        PrimaryKeyConstraint('id', name='tasks_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1,
                                                         maxvalue=9223372036854775807, cycle=False, cache=1),
                                    primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(32))
    status: Mapped[int] = mapped_column(SmallInteger)
    description: Mapped[Optional[str]] = mapped_column(Text)
    deadline: Mapped[Optional[datetime.date]] = mapped_column(Date)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'),
                                                 onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    user: Mapped['User'] = relationship('User', back_populates='tasks')
    files: Mapped[List['File']] = relationship('File', back_populates='task')
