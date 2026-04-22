"""Helper functions"""

import os
import urllib.parse

import requests
import pandas as pd

from sqlalchemy import create_engine, text


def run_sql_query(query: str, params: dict, conn_string: str) -> pd.DataFrame:
    """Execute SQL query with parameters and return DataFrame."""

    encoded_conn_str = urllib.parse.quote_plus(conn_string)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded_conn_str}")

    try:

        with engine.begin() as conn:

            df = pd.read_sql(text(query), conn, params=params)

    except Exception as e:

        print()
        print("SQL error:", e)
        print()

        raise

    return df


def fetch_ats_processes():
    """
    Helper to fetch all active processes in prod Automation Server
    """

    processes = []

    token = os.getenv("ATS_TOKEN")
    url = os.getenv("ATS_URL")

    headers = {"Authorization": f"Bearer {token}"}

    full_url = f"{url}/processes?include_deleted=false"

    response = requests.get(full_url, headers=headers, timeout=60)

    response.raise_for_status()

    res_json = response.json()

    for proc in res_json:
        processes.append(proc.get("name"))

    return processes
