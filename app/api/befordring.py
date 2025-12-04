"""API endpoints for Befordring functionalities."""

from fastapi import APIRouter

from app.utils.database import fetch_child_distance_to_school

router = APIRouter(prefix="/os2forms/api/befordring", tags=["Befordring"])


@router.get("/get_child_distance_to_school/{cpr}")
def get_child_distance_to_school(cpr: str):
    """
    Retrieve a child's distance to school based on their CPR number.
    Distance return is in kilometers.
    """

    child_return = []

    child_data = fetch_child_distance_to_school(cpr=cpr)

    if child_data.empty:
        child_return = ["Kunne udregne barns distance"]

    else:
        distance_in_m = child_data["afstand"].iloc[0]

        distance_in_km = str(round((distance_in_m / 1000), 2))

        child_return = [distance_in_km]

    print(f"child_return: {child_return}")

    return child_return
