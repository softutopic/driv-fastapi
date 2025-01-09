from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, Boolean

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    plate = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    alias = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = Column(Boolean, default=True)

# Pydantic models  
class VehicleBase(BaseModel):
    user_id: uuid.UUID
    plate: str
    year: int
    alias: str
    model_config = ConfigDict(from_attributes=True)
    
class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    plate: Optional[str] = None
    year: Optional[int] = None
    alias: Optional[str] = None
    state: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)
    
class VehicleInDB(VehicleBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    state: bool
    model_config = ConfigDict(from_attributes=True)
