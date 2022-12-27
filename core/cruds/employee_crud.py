from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.schemas.employee import EmployeeCreate, EmployeeUpdate
from core.models import Employee as EmployeeTable
from core.utils.helpers import update_optional_fields


def get_employee(db: Session, employee_id: int):
    return db.query(EmployeeTable).filter(EmployeeTable.id == employee_id).first()


def get_all_employees(db: Session):
    return db.query(EmployeeTable).all()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = EmployeeTable(
        first_name=employee.first_name, last_name=employee.last_name, email=employee.email, phone=employee.phone, address=employee.address,  department=employee.department, lat=employee.lat, lng=employee.lng, is_picked=employee.is_picked)

    if employee.operation_id:
        db_employee.operation_id = employee.operation_id

    db.add(db_employee)
    try:
        db.commit()
        db.refresh(db_employee)
    except Exception as e:
        print(e)
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_employee


def update_employee(db: Session, employee: EmployeeUpdate, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    db_employee = update_optional_fields(db_employee, employee)
    try:
        db.commit()
        db.refresh(db_employee)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_employee


def update_employee_nul_operation(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    db_employee.operation_id = None
    try:
        db.commit()
        db.refresh(db_employee)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return db_employee
