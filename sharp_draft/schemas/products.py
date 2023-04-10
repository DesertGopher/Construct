from pydantic import BaseModel


class ProductList(BaseModel):
    id: int
    name: str
    is_active: int
    category_class_id: int

    class Config:
        orm_mode = True


class ProductBase(ProductList):
    prod_pic: str
    price: float
    measure_id: int
    about: str
    is_stock: int
    vendor: str
    discount: int
