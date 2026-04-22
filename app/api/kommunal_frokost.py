"""API endpoints for Kommunal frokost functionalities."""

from fastapi import APIRouter, HTTPException

from app.utils import database

router = APIRouter(prefix="/os2forms/api/kommunal_frokost", tags=["Kommunal frokost"])


@router.get("/get_dagtilbud")
def get_dagtilbud():
    """
    Endpoint to retrieve all dagtilbud
    """

    dagtilbud_df = database.fetch_dagtilbud()

    dagtilbud = []

    for row in dagtilbud_df.itertuples():
        dagtilbud.append(
            {
                "key": f"{row.LOSID}--{row.DAGTBNR_TXT}--{row.antal_afdelinger}--{row.sdt}",
                # "key": row.LOSID,
                "value": row.DAGTBNR_TXT,
            }
        )

    return dagtilbud


@router.get("/get_dagtilbud_afdelinger/{dagtilbud_losid}")
def get_dagtilbud_afdelinger(dagtilbud_losid: int):
    """
    Endpoint to retrieve all dagtilbud
    """

    dagtilbud_df = database.fetch_dagtilbud_afdelinger(dagtilbud_losid=dagtilbud_losid)

    dagtilbud = []

    for row in dagtilbud_df.itertuples():
        dagtilbud.append(
            {
                "key": row.LOSID,
                "value": row.ENHNAVN,
            }
        )

    return dagtilbud


@router.get("/dagtilbud_info/{dagtilbud_losid}")
def fetch_dagtilbud_info(dagtilbud_losid: int):

    dagtilbud_df = database.dagtilbud_info(dagtilbud_losid=dagtilbud_losid)

    if dagtilbud_df is None or dagtilbud_df.empty:
        raise HTTPException(status_code=404, detail="Dagtilbud not found")

    row = dagtilbud_df.iloc[0]

    val = f"{int(row.antal_afdelinger)}||{bool(row.sdt)}"

    return [{
        "key": val,
        "value": val
    }]
