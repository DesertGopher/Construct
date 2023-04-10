from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Products(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)
    price = Column(Integer)
    is_stock = Column(Integer)
    vendor = Column(String)
    prod_pic = Column(String)
    is_active = Column(Boolean)
    category_class_id = Column(Integer)
    measure_id = Column(Integer)
    discount = Column(Integer)
