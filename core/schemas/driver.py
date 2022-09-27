from pydantic import BaseModel

class DriverCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    address: str
    lat: float
    lng: float
    license_plate: str
    on_operation: bool

    class Config:
        orm_mode = True

class DriverUpdate(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    license_plate: str | None = None
    on_operation: bool | None = None

    class Config:
        orm_mode = True