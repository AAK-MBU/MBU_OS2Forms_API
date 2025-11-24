"""API endpoints for Udskrivning functionalities."""

import os

from io import StringIO

from sqlalchemy import create_engine, text

import urllib.parse

from fastapi import APIRouter

import requests

import pandas as pd

from bs4 import BeautifulSoup

from app.utils.database import fetch_dentist_cvr_data, fetch_citizen_data

router = APIRouter(prefix="/os2forms/api/udskrivning", tags=["Udskrivning"])

@router.get("/get_tandlaeger")
def get_tandlaeger():
    return [{"id": "1", "value": "Hello World"}, {"id": "2", "value": "test"}]

# @router.get("/get_tandlaeger")
# def get_tandlaeger():
#     """
#     Returns a list of dentists in the format:
#     [{"id": <Ydernr>, "value": <Praksisbetegnelse>}]
#     """

#     page_url = "https://medcom.dk/standarder/ydere-lokationsnumre/tandlaeger-i-danmark"
#     headers = {"User-Agent": "Mozilla/5.0"}

#     response = requests.get(page_url, headers=headers, timeout=10)
#     soup = BeautifulSoup(response.text, "html.parser")

#     csv_link = None
#     for a_tag in soup.find_all("a", href=True):
#         if a_tag["href"].endswith(".csv"):
#             csv_link = a_tag["href"]

#             break

#     if not csv_link:
#         return []

#     if csv_link.startswith("/"):
#         csv_link = "https://medcom.dk" + csv_link

#     csv_response = requests.get(csv_link, timeout=10)
#     # csv_response.encoding = "latin1"
#     csv_response.encoding = "utf-8"

#     df = pd.read_csv(StringIO(csv_response.text), sep=";")
#     df = df[["Ydernr", "Praksisbetegnelse", "Adresse", "Postnr", "Post_navn"]]

#     # Drop rows with missing must-have values
#     df = df.dropna(subset=["Praksisbetegnelse", "Adresse"])

#     # Fill optional ones
#     df["Postnr"] = df["Postnr"].fillna("").astype(str).str.replace(".0", "", regex=False)
#     df["Post_navn"] = df["Post_navn"].fillna("").astype(str)

#     dentists = [
#         {
#             "id": str(row["Ydernr"]),
#             "value": f'{row["Praksisbetegnelse"]} || {row["Adresse"]}, {row["Postnr"]} {row["Post_navn"]} || {row["Ydernr"]}'
#         }
#         for _, row in df.iterrows()
#     ]

#     # Sort alphabetically by the 'value' key
#     dentists.sort(key=lambda d: d["value"].lower())

#     return dentists


@router.get("/cvr/{cvr}")
def cvr_check(cvr: str):
    """
    Check if given CVR is valid for dentist.
    If multiple rows: pass if any match valid codes.
    """

    status = ["Ikke godkendt"]

    df = fetch_dentist_cvr_data(cvr=cvr)

    if df.empty:
        status = ["Ikke godkendt"]

    else:
        status = ["Godkendt"]

    return status


@router.get("/citizen/{cpr}")
def get_citizen(cpr: str):
    """
    Retrieve data for a given citizen
    """

    citizen = []

    citizen_data = fetch_citizen_data(cpr=cpr)

    if citizen_data.empty:
        citizen = ["Kunne ikke finde borger i DB"]

    else:
        first_name = citizen_data["firstName"].iloc[0]
        last_name = citizen_data["lastName"].iloc[0]

        citizen = [f"{first_name} {last_name}"]

    return citizen


@router.get("/db-check")
def db_connection_check():
    """
    Simple DB connection check to verify connectivity and authentication.
    """

    conn_str = os.getenv("DBCONNECTIONSTRINGSOLTEQTAND")

    if not conn_str:
        return {"status": "error", "message": "No connection string found in environment."}

    try:
        encoded = urllib.parse.quote_plus(conn_str)
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded}")

        with engine.connect() as conn:
            result = conn.execute(text("SELECT GETDATE() AS current_time")).fetchone()

            return {
                "status": "success",
                "message": "Database connection successful.",
                "current_time": str(result.current_time),
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }
