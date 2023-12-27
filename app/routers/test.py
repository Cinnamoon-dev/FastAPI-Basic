from fastapi import APIRouter

router = APIRouter(prefix="/test")

@router.get("/123")
def test():
    return {"test": "deu bom"}
