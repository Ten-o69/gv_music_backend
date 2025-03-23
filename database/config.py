from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ten_utils.log import Logger

from common.constants import (
    DATABASE_URL,
)


logger = Logger(__name__, level=3)


if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

else:
    logger.error("DATABASE_URL environment variable is not set")
    exit(1)
