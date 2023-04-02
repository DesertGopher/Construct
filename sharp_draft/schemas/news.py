from pydantic import BaseModel


class NewsBase(BaseModel):
    id: int
    title: str
    news: str
    pub_date: str
    picture: str
    is_active: int

    class Config:
        orm_mode = True
