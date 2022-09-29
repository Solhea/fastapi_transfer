from pydantic import BaseModel

from core.utils.enum import Department


class EmployeeCreate(BaseModel):
    firstName: str
    lastName: str
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


class EmployeeUpdate(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
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
