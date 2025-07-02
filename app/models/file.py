from __future__ import annotations

from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Identity, String,
    PrimaryKeyConstraint, ForeignKeyConstraint,
    text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.database import Base


class File(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE', onupdate='CASCADE',
                             name='files_task_id_fkey'),
        PrimaryKeyConstraint('id', name='files_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1,
                                                         maxvalue=9223372036854775807, cycle=False, cache=1),
                                    primary_key=True)
    task_id: Mapped[int] = mapped_column(BigInteger)
    file_path: Mapped[str] = mapped_column(String(255))
    original_name: Mapped[str] = mapped_column(String(64))
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'),
                                                 onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    task: Mapped['Task'] = relationship('Task', back_populates='files')
