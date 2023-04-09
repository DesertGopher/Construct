from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int = None
    name: str = None
    description: str = None

    class Config:
        orm_mode = True


class CategoryExistence(BaseModel):
    id: int = 999
    is_exist: bool = False

    class Config:
        orm_mode = True
