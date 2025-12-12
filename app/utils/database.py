"""Database configuration and connection management."""

import os
import urllib.parse

import pandas as pd

from sqlalchemy import create_engine

DBCONNECTIONSTRINGSERVER29 = os.getenv("DBCONNECTIONSTRINGSERVER29")

DBCONNECTIONSTRINGSOLTEQTAND = os.getenv("DBCONNECTIONSTRINGSOLTEQTAND")

DBCONNECTIONSTRINGPROD = os.getenv("DBCONNECTIONSTRINGPROD")


def fetch_child_distance_to_school(cpr: str) -> pd.DataFrame:
    """
    Fetch child distance to school data from the database by CPR number.
    """

    if not cpr or str(cpr).strip() in ("", "0"):
        return pd.DataFrame()

    query = f"""
        WITH LatestTo AS (
            SELECT
                Cprnr,
                MAX(valid_to_string) AS latest_to
            FROM
                [RPA].[rpa].[Skoleafstand]
            WHERE
                Cprnr = '{cpr}'
            GROUP BY
                Cprnr
        )

        SELECT
            s.*
        FROM
            [RPA].[rpa].[Skoleafstand] s
        INNER JOIN LatestTo l ON s.Cprnr = l.Cprnr AND s.valid_to_string = l.latest_to
        WHERE
            s.Cprnr = '{cpr}'
            AND s.type = 'driving-car'
        """

    encoded_conn_str = urllib.parse.quote_plus(DBCONNECTIONSTRINGPROD)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded_conn_str}")

    try:
        df = pd.read_sql(sql=query, con=engine)

    except Exception as e:
        print("Error during pd.read_sql:", e)

        raise

    return df


def fetch_dentist_cvr_data(cvr: str) -> pd.DataFrame:
    """
    Fetch rows for the CVR with matching industry code.
    """

    query = f"""
        SELECT
            [CVR_nummer],
            [hovedbranche_kode],
            [hovedbranche_kode_0]
        FROM
            [LOIS].[CVR].[JurEnhedKomGeoView]
        WHERE
            CVR_nummer = '{cvr}'
            AND (hovedbranche_kode = '862300' OR hovedbranche_kode_0 = '862300')
    """

    encoded_conn_str = urllib.parse.quote_plus(DBCONNECTIONSTRINGSERVER29)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded_conn_str}")

    try:
        df = pd.read_sql(sql=query, con=engine)

    except Exception as e:
        print("Error during pd.read_sql:", e)

        raise

    return df


def fetch_citizen_data(cpr: str) -> pd.DataFrame:
    """
    Fetch citizen data from Solteq TAND database by CPR number.
    """

    df = pd.DataFrame()

    query = f"""
        SELECT
            patientId,
            firstName,
            lastName,
            cpr
        FROM
            [tmtdata_prod].[dbo].[PATIENT]
        WHERE
            cpr = '{cpr}'
        """

    # Create SQLAlchemy engine
    encoded_conn_str = urllib.parse.quote_plus(DBCONNECTIONSTRINGSOLTEQTAND)

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded_conn_str}")

    try:
        df = pd.read_sql(sql=query, con=engine)

    except Exception as e:
        print("Error during pd.read_sql:", e)

    return df
