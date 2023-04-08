from fastapi import APIRouter, Depends
from sharp_draft.schemas.news import NewsBase
from typing import List

from sharp_draft.service.news_service import NewsService

router = APIRouter(
    prefix='/news',
    tags=["News"],
)


@router.get("/get_last/", response_model=NewsBase)
async def get_product_category_list(
        service: NewsService = Depends()
):
    return service.get_last()
