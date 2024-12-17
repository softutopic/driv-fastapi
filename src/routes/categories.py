import datetime
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.categoryModel import Category, CategoryCreate, CategoryInDB, CategoryUpdate
from dbCon import get_db

category = APIRouter()

@category.post("/api/categories/", response_model=CategoryInDB)
def create_category(category: CategoryCreate, db: Session = Depends()):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@category.get("/api/categories/", response_model=List[CategoryInDB])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@category.get("/api/categories/{category_id}", response_model=CategoryInDB)
def read_category(category_id: uuid.UUID, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.uuid == category_id).first()
    if category is None:
        # return JSONResponse(status_code=404, content="Category not found")
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@category.put("/categories/{category_id}", response_model=CategoryInDB)
def update_category(category_id: uuid.UUID, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.uuid == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db_category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_category)
    return db_category