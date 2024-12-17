from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

Base = declarative_base()

# SQLAlchemy model
class Category(Base):
    __tablename__ = "categories"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = Column(Boolean, default=True)

# Pydantic models
class CategoryBase(BaseModel):
    name: str
    order: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    state: Optional[bool] = None

class CategoryInDB(CategoryBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    state: bool

    class Config:
        orm_mode = True