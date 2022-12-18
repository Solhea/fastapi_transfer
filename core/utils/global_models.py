from pydantic import BaseModel


class delete(BaseModel):
    id: int
    success: bool


class deleted(BaseModel):
    data: delete
