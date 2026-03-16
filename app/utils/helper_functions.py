"""Helper functions"""

import urllib.parse
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
