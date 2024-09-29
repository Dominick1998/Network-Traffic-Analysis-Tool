from sqlalchemy import Column, Integer, String, DateTime
from backend.database import Base

class NetworkTraffic(Base):
    """
    Model for storing network traffic data.
    """
    __tablename__ = 'network_traffic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    protocol = Column(String(50), nullable=False)
    length = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class UserActivity(Base):
    """
    Model for logging user activities in the system.
    """
    __tablename__ = 'user_activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    activity = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
