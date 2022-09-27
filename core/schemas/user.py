from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    firstName: str | None = None
    lastName: str | None = None
    is_active: bool | None = None

    class Config:
        orm_mode = True
