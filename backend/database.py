from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import get_config

# Load configuration based on environment
config = get_config('dev')

# Create a new SQLAlchemy engine
engine = create_engine(config.DATABASE_URI)

# Create a sessionmaker factory
Session = sessionmaker(bind=engine)

def get_db_session():
    """
    Provides a SQLAlchemy session for interacting with the database.
    
    Returns:
        Session: A SQLAlchemy session.
    """
    return Session()
