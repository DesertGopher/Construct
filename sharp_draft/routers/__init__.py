from fastapi import APIRouter
from . import products_routers


router = APIRouter()
router.include_router(products_routers.router)
