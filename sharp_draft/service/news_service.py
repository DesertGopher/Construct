from typing import List

from fastapi import Depends, HTTPException, status

from ..database import get_session
from sqlalchemy.orm import Session

from sharp_draft.models.news_table import News


class NewsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_last(self) -> News:
        """ Метод получения последней активной новости """
        operation = (
            self.session
            .query(News)
            .filter_by(is_active=True)
            .order_by(News.id.desc())
            .first()
        )
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation
