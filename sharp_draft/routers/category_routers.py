from fastapi import APIRouter, Depends
from sharp_draft.schemas.categories import CategoryBase, CategoryExistence
from typing import List

from sharp_draft.service.categories_service import CategoriesService

router = APIRouter(
    prefix='/categories',
    tags=["Categories"],
)


@router.get("/get-list/", response_model=List[CategoryBase])
async def get_categories(
        service: CategoriesService = Depends()
):
    return service.get_category_list()


@router.get("/exist/")
async def is_category_exist(
        name: str,
        service: CategoriesService = Depends()
):
    return service.is_exist(name)

