from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from core.utils.global_models import deleted
from core.utils.helpers import get_db
from core.schemas.operation import OperationGet, OperationGetAll, OperationCreate, OperationUpdate
from core.schemas.employee import EmployeeUpdate
from core.cruds.operation_crud import get_operation, get_all_operations, create_operation, update_operation, delete_operation
from core.cruds.employee_crud import update_employee, get_employee

router = APIRouter(
    prefix="/operation",
    tags=["operations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getOperation/{operation_id}", response_model=OperationGet)
def read_operation(operation_id: int, db: Session = Depends(get_db)):
    db_operation = get_operation(db, operation_id=operation_id)
    if db_operation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")

    return {"data": db_operation}


@router.get("/getOperations", response_model=OperationGetAll)
def read_operations(db: Session = Depends(get_db)):
    db_operations = get_all_operations(db)
    if db_operations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Operations not found")

    return {"data": db_operations}


@router.post("/createOperation", response_model=OperationGet)
def create_operation_route(operation: OperationCreate = Body(embed=False), db: Session = Depends(get_db)):
    db_operation = create_operation(db, operation)

    if db_operation:
        for employee_id in operation.employees:
            if get_employee(db, employee_id=employee_id):
                update_employee(db, EmployeeUpdate(
                    operation_id=db_operation.id), employee_id)
            else:
                delete_operation(db, db_operation.id)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Employee not found",
                )

        db_operation = get_operation(db, operation_id=db_operation.id)

        return {"data": db_operation}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Operation not created",
    )


@router.put("/updateOperation/{operation_id}", response_model=OperationGet)
def update_operation_route(operation_id: int, operation: OperationUpdate = Body(embed=False), db: Session = Depends(get_db)):
    old_operation = get_operation(db, operation_id=operation_id)

    if operation.employees is not None:

        for employee_id in old_operation.employees:
            if get_employee(db, employee_id=employee_id):
                update_employee(db, EmployeeUpdate(
                    operation_id=None), employee_id)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Employee not found",
                )

        for employee_id in operation.employees:
            if get_employee(db, employee_id=employee_id):
                update_employee(db, EmployeeUpdate(
                    operation_id=operation_id), employee_id)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Employee not found",
                )

    db_operation = update_operation(db, operation, operation_id)
    if db_operation:
        return {"data": db_operation}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Operation not updated",
    )


@router.delete("/deleteOperation/{operation_id}", response_model=deleted)
def delete_operation_route(operation_id: int, db: Session = Depends(get_db)):
    db_operation = get_operation(db, operation_id=operation_id)
    if db_operation:
        for employee_id in db_operation.employees:
            if get_employee(db, employee_id=employee_id):
                update_employee(db, EmployeeUpdate(
                    operation_id=None), employee_id)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Employee not found",
                )

        db_operation = delete_operation(db, operation_id)
        if db_operation:
            return {"data": {"id": operation_id, "success": True}}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Operation not deleted",
    )
