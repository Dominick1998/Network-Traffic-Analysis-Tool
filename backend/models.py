from sqlalchemy import Column, Integer, String, DateTime
from backend.database import Base

class NetworkTraffic(Base):
    __tablename__ = 'network_traffic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    protocol = Column(String(50), nullable=False)
    length = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class UserActivity(Base):
    __tablename__ = 'user_activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    activity = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    condition = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

class AnomalyLog(Base):
    __tablename__ = 'anomaly_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_ip = Column(String(255), nullable=False)
    destination_ip = Column(String(255), nullable=False)
    protocol = Column(String(50), nullable=False)
    length = Column(Integer, nullable=False)
    anomaly_type = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String(255), nullable=False)
    notification_type = Column(String(50), nullable=False, default='info')
    created_at = Column(DateTime, nullable=False)

class IncidentReport(Base):
    __tablename__ = 'incident_reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    severity = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)

class ThreatLog(Base):
    """
    Model for storing detected threat information.
    """
    __tablename__ = 'threat_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    threat_type = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, nullable=False)
