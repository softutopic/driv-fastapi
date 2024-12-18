import uuid
from dbCon import Base
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, DateTime
# from src.models.subcategoryModel import Subcategory

# SQLAlchemy model
class Category(Base):
    __tablename__ = "categories"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = Column(Boolean, default=True)
    
    # subcategories = relationship(Subcategory, back_populates="category")

# Pydantic models
class CategoryBase(BaseModel):
    name: str
    order: int
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    state: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryInDB(CategoryBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    state: bool
    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     orm_mode = True