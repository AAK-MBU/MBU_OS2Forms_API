"""API endpoints for Befordring functionalities."""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import APIRouter

from app.utils import database

router = APIRouter(prefix="/os2forms/api/befordring", tags=["Befordring"])


@router.get("/get_child_distance_to_school/{cpr}/{month_year}")
def get_child_distance_to_school(cpr: str, month_year: str):
    """
    API endpoint to fetch a childs distance to school
    """

    string_cpr = str(cpr)

    child_data = database.fetch_child_distance_to_school(
        cpr=string_cpr,
        month_year=month_year,
    )

    rows = child_data["TidspunktForBevilling"].tolist()

    if not rows:
        return [{"value": "Kunne ikke udregne barns distance"}]

    if "Morgen og eftermiddag" in rows:
        if len(rows) > 1:
            return [{"value": "Kunne ikke udregne barns distance"}]

    else:
        if rows.count("Morgen") > 1 or rows.count("Eftermiddag") > 1:
            return [{"value": "Kunne ikke udregne barns distance"}]

    distance = child_data["BevilgetKoereAfstand"].iloc[0]

    return [{"value": str(distance)}]


@router.get("/get_reporting_months")
def get_reporting_months():
    """
    Return the current month and the previous 4 months
    for OS2Forms dropdown selection.
    """

    months = []

    month_names_da = {
        1: "Januar",
        2: "Februar",
        3: "Marts",
        4: "April",
        5: "Maj",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "December",
    }

    today = datetime.today()

    for i in range(5):

        date = today - relativedelta(months=i)

        key = date.strftime("%Y-%m")
        value = f"{month_names_da[date.month]} {date.year}"

        months.append(
            {
                "key": key,
                "value": value
            }
        )

    return months
