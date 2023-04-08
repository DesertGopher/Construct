from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int = None
    name: str = None
    description: str = None

    class Config:
        orm_mode = True
