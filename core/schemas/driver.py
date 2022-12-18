from pydantic import BaseModel

from core.utils.helpers import to_camel


class Driver(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    lat: float
    lng: float
    license_plate: str
    on_operation: bool

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class DriverGet(BaseModel):
    data: Driver


class DriverGetAll(BaseModel):
    data: list[Driver]


class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    lat: float
    lng: float
    license_plate: str
    on_operation: bool

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class DriverUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    license_plate: str | None = None
    on_operation: bool | None = None

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
