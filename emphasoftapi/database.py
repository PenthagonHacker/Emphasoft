import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, unique=False, index=True, nullable=True)
    last_name = Column(String, unique=False, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.datetime.utcnow())
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String)


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True, nullable=False, index=True)
    expires = Column(DateTime)
    user_id = Column(ForeignKey('users.id'))
