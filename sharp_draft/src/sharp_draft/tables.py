from sqlalchemy import (
    Column,
    Date,
    Boolean,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    news = Column(String)
    pub_date = Column(DateTime)
    picture = Column(String)
    is_active = Column(Boolean)
