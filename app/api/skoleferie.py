"""API endpoints for Skoleferie functionalities."""

from fastapi import APIRouter

router = APIRouter(prefix="/os2forms/api/skoleferie", tags=["Skoleferie"])


@router.get("/")
def get_skoleferie():
    return {"status": "ok", "data": "Skoleferie info here"}
