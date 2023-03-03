from fastapi import APIRouter, Depends
from sharp_draft.schemas.products import ProductBase
from typing import List

from sharp_draft.service.products_service import ProductsService

router = APIRouter(
    prefix='/products'
)


@router.get("/{product_id}/", response_model=ProductBase)
async def get_product_id(
        product_id: int,
        service: ProductsService = Depends()
):
    return service.get(product_id)
