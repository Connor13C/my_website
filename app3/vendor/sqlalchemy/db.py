import os

from sqlalchemy import engine
from sqlalchemy.orm import DeclarativeBase

db = engine(os.environ.get('DATABASE_URL'), echo=True)
Base = DeclarativeBase(bind=db)
