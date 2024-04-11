import pandas as pd
import sqlite3


def insert_expense(
    conn, date, amount, category, sub_category, comment, expense_type, account_name
):
    c = conn.cursor()
    c.execute(
        """
    INSERT INTO expenses (date, amount, category, sub_category, comment, type, account_name)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (date, amount, category, sub_category, comment, expense_type, account_name),
    )
    conn.commit()


def get_dataframe(conn):
    # Read data from SQLite into a Pandas DataFrame
    query = "SELECT * FROM expenses;"
    df = pd.read_sql_query(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    # Set the 'date' column as the index
    # df.set_index('date', inplace=True)
    # Reset the index
    # df.reset_index(inplace=True)
    return df
