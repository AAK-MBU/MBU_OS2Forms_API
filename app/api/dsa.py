"""API endpoints for DSA functionalities."""

from fastapi import APIRouter

from app.utils import database

router = APIRouter(prefix="/os2forms/api/dsa", tags=["DSA"])


@router.get("/get_child_modersmaal/{cpr}")
def get_child_modersmaal(cpr: str):
    """
    API endpoint to fetch a childs modersmaal
    """

    string_cpr = str(cpr)

    child_data = database.fetch_child_modersmaal(cpr=string_cpr)

    if child_data.empty:
        return [{"value": "Kunne ikke finde barnets modersmaal"}]

    modersmaal = child_data["modersmaal"]

    if modersmaal.nunique(dropna=False) > 1:
        return [{"value": "Kunne ikke finde barnets modersmaal"}]

    return [{"value": str(modersmaal.iloc[0])}]
