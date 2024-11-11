from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/health", status_code=200)
async def health():
    return {"status": "ok"}
