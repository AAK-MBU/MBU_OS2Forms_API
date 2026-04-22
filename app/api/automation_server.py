"""API endpoints for Kommunal frokost functionalities."""

from fastapi import APIRouter

from app.utils import helper_functions

router = APIRouter(prefix="/os2forms/api/automation_server", tags=["Automation server"])


@router.get("/get_processes")
def get_processes():
    """
    Endpoint to retrieve all dagtilbud
    """

    processes = helper_functions.fetch_ats_processes()

    processes.sort()

    return processes
