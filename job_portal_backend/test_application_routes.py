from fastapi import APIRouter

# Test router
router = APIRouter(prefix="/api/applications", tags=["Applications"])

@router.get("/test")
async def test_route():
    return {"message": "test"}
