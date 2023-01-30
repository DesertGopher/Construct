from pydantic import BaseModel
from datetime import datetime


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class News(OurBaseModel):
    id: str
    title: str
    news: str
    pub_date = str
    picture = str
    is_active = str
