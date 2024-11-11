from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency to get a database connection
    
    Returns: 
    sqlalchemy.orm.session.Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
