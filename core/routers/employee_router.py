from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from core.utils.helpers import get_db
from core.schemas.employee import EmployeeCreate, EmployeeUpdate
from core.cruds.employee_crud import get_employee, get_all_employees, create_employee, update_employee, delete_employee


router = APIRouter(
    prefix="/employee",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getEmployee/{employee_id}")
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    return {"data": db_employee}


@router.get("/getEmployees")
def read_employees(db: Session = Depends(get_db)):
    db_employees = get_all_employees(db)
    if db_employees is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employees not found")

    return {"data": db_employees}


@router.post("/createEmployee")
def create_employee_route(employee: EmployeeCreate = Body(embed=False), db: Session = Depends(get_db)):

    db_employee = create_employee(db, employee)
    if db_employee:
        return {"data": db_employee}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Employee not created",
    )


@router.put("/updateEmployee/{employee_id}")
def update_employee_route(employee_id: int, employee: EmployeeUpdate = Body(embed=False), db: Session = Depends(get_db)):
    db_employee = update_employee(db, employee, employee_id)
    if db_employee:
        return {"data": db_employee}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Employee not updated",
    )


@router.delete("/deleteEmployee/{employee_id}")
def delete_employee_route(employee_id: int, db: Session = Depends(get_db)):
    db_employee = delete_employee(db, employee_id)
    if db_employee:
        return {"data": True}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Employee not deleted",
    )
