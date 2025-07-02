from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from contextlib import contextmanager

from dotenv import load_dotenv

import os


class Base(DeclarativeBase):
    pass


load_dotenv()

DB_URL = f"{os.getenv('DATABASE_URL').strip()}/{os.getenv('DATABASE_NAME').strip()}"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
