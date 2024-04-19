import streamlit as st
import pandas as pd
import expenses_tracker.database as database
import sqlite3

import yaml

# Load category and subcategory names from the YAML file
with open("config.yaml", "r") as file:
    data = yaml.safe_load(file)

categories = list(data["categories"].keys())
income_categories = list(data["income_categories"].keys())
accounts_liquid = list(data["accounts"]["liquid"])

# Streamlit code to insert new rows using form submission
st.title("Expense Tracker s")


def main():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    # Create the expenses table if it doesn't already exist
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        amount REAL,
        category TEXT,
        sub_category TEXT,
        comment TEXT,
        type TEXT,
        account_name TEXT
    )
    """
    )
    expense_type = st.selectbox("Expense Type", ["Expense", "\U0001F4B2 Income"])
    with st.container(border=True):
        if expense_type == "Expense":
            category = st.selectbox(
                "Category", categories
            )  # Deve stare fuori dal form altrimenti non si aggiornano le sub_categories
            category_type = "categories"
        elif expense_type == "\U0001F4B2 Income":
            category = st.selectbox(
                "Category", income_categories
            )  # Deve stare fuori dal form altrimenti non si aggiornano le sub_categories
            category_type = "income_categories"

        sub_categories = list(data[category_type][category])
        with st.form(key="expense_form", border=False):
            sub_category = st.selectbox("Subcategory", sub_categories)
            date = st.date_input("Date", format="DD/MM/YYYY")
            amount = st.number_input("Amount", value=0.0, step=0.01)
            comment = st.text_area("Comment")
            account_name = st.selectbox("Account Name", accounts_liquid)

            submit_button = st.form_submit_button(
                label="Add Expense", type="primary"
            )

            if submit_button:
                database.insert_expense(
                conn,
                date,
                amount,
                category,
                sub_category,
                comment,
                expense_type,
                account_name,
                )
                st.success("Expense added successfully!")
    

    df = database.get_dataframe(conn)
    st.session_state["df"] = df
    COLUMN_CONFIG = {
        "id": None,
        "date": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
        "category": "Categoria",
        "sub_category": "Sotto categoria",
        "comment": "Commento",
        "account_name": "Conto",
        "type": None,
        "amount": st.column_config.NumberColumn("Importo", format="%.2f"),
    }
    st.header("Ultimi 10 pagamenti aggiunti")
    st.dataframe(
        df.tail(10), use_container_width=True, hide_index=True, column_config=COLUMN_CONFIG
    )
    st.header("Ultimi 10 pagamenti aggiunti")
    df_expenses = df.loc[(df["type"] == "Expense")]
    st.dataframe(
        df_expenses.tail(10),
        use_container_width=True,
        hide_index=True,
        column_config=COLUMN_CONFIG,
    )
    st.header("Ultimi 10 d aggiunti")
    df_income = df.loc[(df["type"] == "\U0001F4B2 Income")]
    st.dataframe(
        df_income.tail(10),
        use_container_width=True,
        hide_index=True,
        column_config=COLUMN_CONFIG,
    )

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
