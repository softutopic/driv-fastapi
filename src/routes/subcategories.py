from datetime import datetime
from typing import Annotated, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dbCon import get_db
from src.models.categoryModel import Category
from src.models.subcategoryModel import SubcategoryCreate, SubcategoryInDB, Subcategory, SubcategoryUpdate

subcategoryRoute = APIRouter()
DbDependency = Annotated[Session, Depends(get_db)]

@subcategoryRoute.post("/api/subcategories/", response_model=SubcategoryInDB)
def create_subcategory(subcategory_data: SubcategoryCreate, db: DbDependency):
    # Verify that the category exists
    category = db.query(Category).filter(
        Category.uuid == subcategory_data.category_uuid
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with uuid {subcategory_data.category_uuid} not found"
        )

    try:
        # Creamos una nueva instancia de Subcategory usando los datos del modelo Pydantic
        db_subcategory = Subcategory(
            name=subcategory_data.name,
            order=subcategory_data.order,
            category_uuid=subcategory_data.category_uuid
        )
        
        db.add(db_subcategory)
        db.commit()
        db.refresh(db_subcategory)
        return db_subcategory
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating subcategory: {str(e)}"
        )

@subcategoryRoute.get("/api/subcategories/", response_model=List[SubcategoryInDB])
def read_subcategories(
    skip: int = 0, 
    limit: int = 100, 
    category_uuid: Optional[uuid.UUID] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Subcategory)
    if category_uuid:
        query = query.filter(Subcategory.category_uuid == category_uuid)
    return query.offset(skip).limit(limit).all()

@subcategoryRoute.get("/api/subcategories/{subcategory_id}", response_model=SubcategoryInDB)
async def read_subcategory(subcategory_id: uuid.UUID, db: DbDependency):
    subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if subcategory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Subcategory with uuid {subcategory_id} not found"
        )
    return subcategory

@subcategoryRoute.put("/api/subcategories/{subcategory_id}", response_model=SubcategoryInDB)
async def update_subcategory(
    subcategory_id: uuid.UUID, 
    subcategory: SubcategoryUpdate, 
    db: DbDependency
):
    db_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if db_subcategory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Subcategory with uuid {subcategory_id} not found"
        )
    
    update_data = subcategory.model_dump(exclude_unset=True)
    
    # If category_uuid is being updated, verify the new category exists
    if "category_uuid" in update_data:
        category = db.query(Category).filter(Category.uuid == update_data["category_uuid"]).first()
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with uuid {update_data['category_uuid']} not found"
            )
    
    for key, value in update_data.items():
        setattr(db_subcategory, key, value)
    
    db_subcategory.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

@subcategoryRoute.delete("/api/subcategories/{subcategory_id}", response_model=SubcategoryInDB)
async def delete_subcategory(subcategory_id: uuid.UUID, db: DbDependency):
    subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if subcategory is None:
        raise HTTPException(
            status_code=404,
            detail=f"Subcategory with uuid {subcategory_id} not found"
        )
    
    db.delete(subcategory)
    db.commit()
    return subcategory