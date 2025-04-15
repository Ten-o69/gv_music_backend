from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from common.constants import (
    DATABASE_URL,
    DATABASE_LOG,
)


engine = create_engine(DATABASE_URL, echo=DATABASE_LOG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
