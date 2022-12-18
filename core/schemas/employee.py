from pydantic import BaseModel

from core.utils.helpers import to_camel
from core.utils.enum import Department


class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    lat: float
    lng: float
    is_picked: bool
    operation_id: int | None = None
    department: Department

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class EmployeeGet(BaseModel):
    data: Employee


class EmployeeGetAll(BaseModel):
    data: list[Employee]


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    lat: float
    lng: float
    is_picked: bool
    operation_id: int | None = None
    department: Department

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    is_picked: bool | None = None
    operation_id: int | None = None
    department: Department | None = None

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
