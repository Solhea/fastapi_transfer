from pydantic import BaseModel
from datetime import datetime

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