from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.new, nullable=False)
    source = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
