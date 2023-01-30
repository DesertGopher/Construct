from fastapi import APIRouter
from .. import tables
from ..database import Session
from ..models.operations import News
from typing import List


router = APIRouter(
    prefix='/operations'
)


@router.get('/', response_model=List[News])
def get_operations():
    session = Session()
    operations = (session.query(tables.News).all())
    return operations
