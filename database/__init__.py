from .config import Base, engine, SessionLocal


def init_db():
    Base.metadata.create_all(engine)


init_db()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
