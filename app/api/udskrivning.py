from fastapi import APIRouter

router = APIRouter(prefix="/os2forms/api/udskrivning", tags=["Udskrivning"])


@router.get("/")
def get_udskrivning():
    return {"status": "ok", "data": "Udskrivning info here"}
