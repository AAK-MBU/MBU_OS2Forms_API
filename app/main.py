from fastapi import FastAPI
from app.api import befordring, udskrivning, skoleferie

app = FastAPI(
    title="MBU OS2Forms API",
    description="Simple API for OS2Forms integrations",
    version="1.0.0"
)

app.include_router(befordring.router)
app.include_router(udskrivning.router)
app.include_router(skoleferie.router)


@app.get("/")
def root():
    return {"message": "MBU OS2Forms API is running"}


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}