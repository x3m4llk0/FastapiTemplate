from uuid import uuid4

from fastapi import APIRouter

from app.database.data_layer.test_dao import TestDAO
from app.schemas.tests import TestDTO

router = APIRouter(tags=["Test"], prefix="/test")


@router.get('')
async def test_router():
    return {"response:": "test success"}




@router.post('', response_model=TestDTO)
async def test_add_item(info: str):
    result = await TestDAO.create(info=info)
    return result