from fastapi import APIRouter
from . import news


router = APIRouter()
router.include_router(news.router)
