from pydantic import BaseModel


class ProductList(BaseModel):
    id: int
    name: str
    price: float
    is_active: int
    measure_id: int

    class Config:
        orm_mode = True


class ProductBase(ProductList):
    prod_pic: str
    category_class_id: int
