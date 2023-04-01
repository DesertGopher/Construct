from typing import List

from fastapi import Depends, HTTPException, status

from ..database import get_session
from sqlalchemy.orm import Session

from sharp_draft.models.products_table import Products


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, product_id: int) -> Products:
        """ Метод получения продукта по id выносим для использования в других методах """
        operation = (
            self.session
            .query(Products)
            .filter_by(id=product_id)
            .first()
        )
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get(self, product_id: int) -> Products:
        """ Получение продукта по id """
        return self._get(product_id)

    def get_by_category(self, category: int) -> dict:
        """ Метод получения списка товаров по категории"""
        operations = (
            self.session
            .query(Products)
            .filter_by(category_class_id=category)
            .all()
        )
        if not operations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operations
