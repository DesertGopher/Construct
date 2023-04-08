from typing import List

from fastapi import Depends, HTTPException, status

from ..database import get_session
from sqlalchemy.orm import Session

from sharp_draft.models.categories_table import Categories


class CategoriesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_category_list(self) -> List:
        """ Метод получения списка категорий """
        operation = self.session.query(Categories).all()
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation
