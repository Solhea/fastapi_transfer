from pydantic import BaseModel

class DriverCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    address: str
    lat: float
    lng: float
    licensePlate: str
    onOperation: bool

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
    licensePlate: str | None = None
    onOperation: bool | None = None

    class Config:
        orm_mode = True