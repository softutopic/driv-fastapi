import uuid
from dbCon import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import relationship
from src.models.categoryModel import CategoryBase, Category
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String

class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    order = Column(Integer)
    category_uuid = Column(UUID(as_uuid=True), ForeignKey('categories.uuid', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = Column(Boolean, default=True)

    # category = relationship(Category, back_populates="subcategories")

# Subcategory schemas (new)
class SubcategoryBase(BaseModel):
    name: str
    order: int
    category_uuid: uuid.UUID

class SubcategoryCreate(SubcategoryBase):
    pass

class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    category_uuid: Optional[uuid.UUID] = None
    state: Optional[bool] = None

class SubcategoryInDB(SubcategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    state: bool

    class Config:
        orm_mode = True

class CategoryInDB(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    state: bool
    subcategories: List[SubcategoryInDB] = []

    class Config:
        orm_mode = True