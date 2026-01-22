# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = (
    f"mysql+pymysql://{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
