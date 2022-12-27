from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.schemas.operation import OperationCreate, OperationUpdate
from core.models import Operation as OperationTable
from core.utils.helpers import update_optional_fields


def get_operation(db: Session, operation_id: int):
    return db.query(OperationTable).filter(OperationTable.id == operation_id).first()


def get_all_operations(db: Session):
    return db.query(OperationTable).all()


def create_operation(db: Session, operation: OperationCreate):
    db_operation = OperationTable(
        name=operation.name, description=operation.description, driver_id=operation.driver_id, start_time=operation.start_time, end_time=operation.end_time, is_finished=operation.is_finished)
    db.add(db_operation)
    try:
        db.commit()
        db.refresh(db_operation)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on name")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_operation


def update_operation(db: Session, operation: OperationUpdate, operation_id: int):
    db_operation = get_operation(db, operation_id)
    if not db_operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")

    # delete employees we can't update them here
    if operation.employees:
        del operation.employees

    db_operation = update_optional_fields(db_operation, operation)

    try:
        db.commit()
        db.refresh(db_operation)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on name")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_operation


def delete_operation(db: Session, operation_id: int):
    db_operation = get_operation(db, operation_id)
    if not db_operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    db.delete(db_operation)
    db.commit()
    return db_operation
