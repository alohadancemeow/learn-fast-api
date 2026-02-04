from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLAlchemy setup
# The database URL is fetched from application settings for flexibility.
engine = create_engine(settings.database_url)

# SessionLocal is a factory for new Session objects.
# It's configured to not commit until explicitly told to do so (autocommit=False)
# and to not flush until explicitly told to do so (autoflush=False).
# This provides transaction isolation for each request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class for our declarative models.
# All SQLAlchemy models will inherit from this Base.
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a SQLAlchemy session for a single request.
    It ensures that the database session is closed after the request is finished,
    regardless of whether the request was successful or encountered an error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
