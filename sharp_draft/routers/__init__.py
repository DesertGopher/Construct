from fastapi import APIRouter
from . import (
    products_routers,
    news_routers,
    category_routers,
)


router = APIRouter()
router.include_router(products_routers.router)
router.include_router(news_routers.router)
router.include_router(category_routers.router)
