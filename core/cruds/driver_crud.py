from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.schemas.driver import DriverCreate, DriverUpdate
from core.models import Driver as DriverTable
from core.utils.helpers import update_optional_fields


def get_driver(db: Session, driver_id: int):
    return db.query(DriverTable).filter(DriverTable.id == driver_id).first()


def get_all_drivers(db: Session):
    return db.query(DriverTable).all()


def create_driver(db: Session, driver: DriverCreate):
    db_driver = DriverTable(
        first_name=driver.first_name, last_name=driver.last_name, email=driver.email, phone=driver.phone, address=driver.address,  lat=driver.lat, lng=driver.lng, license_plate=driver.license_plate, on_operation=driver.on_operation)
    db.add(db_driver)
    try:
        db.commit()
        db.refresh(db_driver)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_driver


def update_driver(db: Session, driver: DriverUpdate, driver_id: int):
    db_driver = get_driver(db, driver_id)
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

    db_driver = update_optional_fields(db_driver, driver)
    try:
        db.commit()
        db.refresh(db_driver)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_driver


def delete_driver(db: Session, driver_id: int):
    db_driver = get_driver(db, driver_id)
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    db.delete(db_driver)
    db.commit()
    return db_driver
