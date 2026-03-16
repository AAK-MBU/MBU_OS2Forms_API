"""Database configuration and connection management."""

import os
import urllib.parse

from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from sqlalchemy import create_engine

from app.utils import helper_functions

DBCONNECTIONSTRINGSERVER29 = os.getenv("DBCONNECTIONSTRINGSERVER29")

DBCONNECTIONSTRINGSOLTEQTAND = os.getenv("DBCONNECTIONSTRINGSOLTEQTAND")

DBCONNECTIONSTRINGPROD = os.getenv("DBCONNECTIONSTRINGPROD")


def fetch_child_distance_to_school(cpr: str, month_year: str):
    """
    Fetch a childs befordrings data
    """

    cpr = str(cpr).strip()

    if not cpr or cpr == "0":
        return pd.DataFrame()

    try:
        start_date = datetime.strptime(month_year, "%Y-%m")
    except ValueError:
        return pd.DataFrame()

    end_date = start_date + relativedelta(months=1, days=-1)

    query = """
        SELECT
            TidspunktForBevilling,
            BevilgetKoereAfstand
        FROM
            RPA.rpa.BefordringsData
        WHERE
            CPR = :cpr
            AND BevillingAfKoerselstype = 'Egenbefordring'
            AND BevillingFra <= :month_end
            AND BevillingTil >= :month_start
    """

    params = {
        "cpr": cpr,
        "month_start": start_date.date(),
        "month_end": end_date.date(),
    }

    return helper_functions.run_sql_query(
        query=query,
        params=params,
        conn_string=DBCONNECTIONSTRINGPROD
    )


def fetch_dentist_cvr_data(cvr: str) -> pd.DataFrame:
    """
    Fetch rows for the CVR with matching industry code.
    """

    query = f"""
        SELECT
            jw.[CVR_nummer],
            jw.[hovedbranche_kode],
            jw.[hovedbranche_kode_0],
            pw.[CVR_nummer],
            pw.[hovedbranche_kode],
            pw.[hovedbranche_kode_0]
        FROM
            [LOIS].[CVR].[JurEnhedKomGeoView] jw
        FULL OUTER JOIN
            [LOIS].[CVR].[ProdEnhedGeoView] pw ON jw.CVR_nummer = pw.CVR_nummer
        WHERE
            (jw.CVR_nummer = '{cvr}' or pw.CVR_nummer = '{cvr}')
            AND
            (pw.hovedbranche_kode = '862300' OR jw.hovedbranche_kode_0 = '862300' or pw.hovedbranche_kode = '862300' OR pw.hovedbranche_kode_0 = '862300')
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
