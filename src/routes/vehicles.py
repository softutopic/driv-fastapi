from typing import Annotated, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dbCon import get_db
from src.models.vehicleModel import VehicleInDB, Vehicle, VehicleCreate, VehicleUpdate


vehicleRoute = APIRouter()
DbDependency = Annotated[Session, Depends(get_db)]

@vehicleRoute.get("/api/vehicles/", response_model=List[VehicleInDB])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Vehicle).offset(skip).limit(limit).all()

@vehicleRoute.get("/api/vehicles/{vehicle_id}", response_model=VehicleInDB)
def read_vehicle(vehicle_id: uuid.UUID, db: DbDependency):
    vehicle = db.query(Vehicle).filter(Vehicle.uuid == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@vehicleRoute.post("/api/vehicles/", response_model=VehicleInDB)
def create_vehicle(vehicle: VehicleCreate, db: DbDependency):
    db_vehicle = Vehicle(
        user_id=vehicle.user_id,
        plate=vehicle.plate,
        year=vehicle.year,
        alias=vehicle.alias
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@vehicleRoute.put("/api/vehicles/{vehicle_id}", response_model=VehicleInDB)
def update_vehicle(vehicle_id: uuid.UUID, vehicle: VehicleUpdate, db: DbDependency):
    db_vehicle = db.query(Vehicle).filter(Vehicle.uuid == vehicle_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    update_data = vehicle.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vehicle, key, value)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@vehicleRoute.delete("/api/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: uuid.UUID, db: DbDependency):
    db_vehicle = db.query(Vehicle).filter(Vehicle.uuid == vehicle_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}