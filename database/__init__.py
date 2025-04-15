from .config import Base, engine, SessionLocal


def init_db():
    """
    Initializes the database by creating all tables defined in the metadata.

    This function should be called once during application startup to ensure
    that all models mapped to the SQLAlchemy `Base` are created in the database.
    """
    Base.metadata.create_all(engine)

# Initialize the database when the module is imported
init_db()


def get_db():
    """
    Dependency function for retrieving a database session.

    Used in FastAPI routes to provide a scoped SQLAlchemy session. Ensures that
    the session is properly closed after the request is completed.

    Yields:
        Session: A SQLAlchemy database session object.

    Example:
        Usage in FastAPI endpoint:

        from fastapi import Depends
        from sqlalchemy.orm import Session

        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
