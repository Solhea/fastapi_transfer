from pydantic import BaseModel
from datetime import datetime

from core.utils.helpers import to_camel
from core.schemas.employee import Employee
from core.schemas.driver import Driver


class Operation(BaseModel):
    id: int
    name: str
    description: str
    driver: Driver
    start_time: datetime
    end_time: datetime
    is_finished: bool
    employees: list[Employee]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class OperationGet(BaseModel):
    data: Operation


class OperationGetAll(BaseModel):
    data: list[Operation]


class OperationCreate(BaseModel):
    name: str
    description: str
    driver_id: int
    start_time: datetime
    end_time: datetime
    is_finished: bool
    employees: list[int]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class OperationUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    driver_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    is_finished: bool | None = None
    employees: list[int] | None = None

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
