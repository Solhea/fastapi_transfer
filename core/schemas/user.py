from pydantic import BaseModel

from core.utils.helpers import to_camel


class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserGet(BaseModel):
    data: User


class UserGetAll(BaseModel):
    data: list[User]


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
