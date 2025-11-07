from fastapi import APIRouter

router = APIRouter(prefix="/os2forms/api/befordring", tags=["Befordring"])

@router.get("/")
def get_befordring():
    return {"status": "ok", "data": "Befordring info here"}
