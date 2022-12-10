from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from core.utils.helpers import get_db
from core.schemas.driver import DriverCreate, DriverUpdate
from core.cruds.driver_crud import get_driver, get_all_drivers, create_driver, update_driver, delete_driver
from core.middleware import hash_password, get_current_user


router = APIRouter(
    prefix="/driver",
    tags=["drivers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getDriver/{driver_id}")
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = get_driver(db, driver_id=driver_id)
    if db_driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

    return {"data": db_driver}


@router.get("/getDrivers")
def read_drivers(db: Session = Depends(get_db)):
    db_drivers = get_all_drivers(db)
    if db_drivers is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Drivers not found")

    return {"data": db_drivers}


@router.post("/createDriver")
def create_driver_route(driver: DriverCreate = Body(embed=False), db: Session = Depends(get_db)):
    db_driver = create_driver(db, driver)
    if db_driver:
        return {"data": db_driver}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Driver not created",
    )


@router.put("/updateDriver/{driver_id}")
def update_driver_route(driver_id: int, driver: DriverUpdate = Body(embed=False), db: Session = Depends(get_db)):
    db_driver = update_driver(db, driver, driver_id)
    if db_driver:
        return {"data": db_driver}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Driver not updated",
    )


@router.delete("/deleteDriver/{driver_id}")
def delete_driver_route(driver_id: int, db: Session = Depends(get_db)):
    db_driver = delete_driver(db, driver_id)
    if db_driver:
        return {"data": True}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Driver not deleted",
    )
