from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args=settings.DATABASE_CONNECT_ARGS)


def init_db():
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for getting database sessions."""
    with Session(engine) as session:
        yield session