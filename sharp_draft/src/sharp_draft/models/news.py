from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    id: int
    title: str
    news: str
    pub_date: datetime
    picture: str
    is_active: int

    class Config:
        orm_mode = True
