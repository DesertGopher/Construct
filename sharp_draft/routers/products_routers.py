from fastapi import APIRouter, Depends
from sharp_draft.schemas.products import ProductBase
from typing import List

from sharp_draft.service.products_service import ProductsService

router = APIRouter(
    prefix='/products'
)


@router.get("/category/{category}/", response_model=List[ProductBase])
async def get_product_category_list(
        category: int,
        service: ProductsService = Depends()
):
    return service.get_by_category(category)


@router.get("/{product_id}/", response_model=ProductBase)
async def get_product_id(
        product_id: int,
        service: ProductsService = Depends()
):
    return service.get(product_id)

