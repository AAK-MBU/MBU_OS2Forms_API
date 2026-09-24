"""API endpoints for Processes functionalities."""

from fastapi import APIRouter

from app.utils import database

router = APIRouter(prefix="/os2forms/api/processes", tags=["Processes"])


@router.get("/get_processes")
def get_processes(process_type: str | None = None):
    """
    Return all processes as key/value pairs for OS2Forms dropdowns.
    Optionally filter by process type ('RPA' or 'Formular')
    via the process_type query param.
    """

    processes_df = database.fetch_processes(process_type=process_type)

    processes = []

    for row in processes_df.itertuples():
        processes.append(
            {
                "key": row.processId,
                "value": f"{row.department}: {row.name}",
            }
        )

    return processes
