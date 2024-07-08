from fastapi import APIRouter

router = APIRouter(tags=["Test"], prefix="/test")


@router.get('')
def test_router():
    return {"response:": "test success"}
