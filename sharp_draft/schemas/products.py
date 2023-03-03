from pydantic import BaseModel


class ProductBase(BaseModel):
    id: int
    name: str
    price: float
    prod_pic: str
    is_active: int
    category_class_id: int
    measure_id: int

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass
