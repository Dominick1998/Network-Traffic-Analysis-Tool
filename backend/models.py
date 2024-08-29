from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for our SQLAlchemy models
Base = declarative_base()

class NetworkTraffic(Base):
    """
    Model representing a captured network traffic packet.
    """
    __tablename__ = 'network_traffic'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    protocol = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NetworkTraffic(id={self.id}, source={self.source}, destination={self.destination}, protocol={self.protocol}, length={self.length}, timestamp={self.timestamp})>"

# Create the table schema
def create_tables(engine):
    """
    Create all tables in the database.

    Args:
        engine: The SQLAlchemy engine to connect to the database.
    
    Returns:
        None
    """
    Base.metadata.create_all(engine)
