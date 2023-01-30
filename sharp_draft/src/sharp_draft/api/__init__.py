from fastapi import APIRouter
from .operations import router as operations_router


router = APIRouter()
router.include_router(operations_router)
