import plotly.express as px
import streamlit as st
import pandas as pd

df = st.session_state["df"]

range_time_selected = st.radio(
    "Seleziona il raggruppamento dei grafici",
    options=["Mensile", "Annuale"],
    horizontal=True,
    index=None,
)

if range_time_selected == "Mensile":
    year_selected = st.selectbox(
        label="Seleziona l'anno di riferimento", options=df["date"].dt.year.unique()
    )
    # ENTRATE USCITE PER MESE
    df_filtered = df.loc[
        (df["type"].isin(["Expense", "\U0001F4B2 Income"]))
        & (df["date"].dt.year == year_selected)
    ]

    df_filtered["month_name"] = df_filtered["date"].dt.strftime("%b")
    df_grouped = (
        df_filtered.groupby(["month_name", "type"])["amount"].sum().reset_index()
    )
    fig = px.bar(
        data_frame=df_grouped,
        x="month_name",
        y="amount",
        color="type",
        barmode="group",
        labels={
            "amount": "Totale spese",
            "month_name": "Mese",
            "type": "Entrate o uscite",
        },
        title=f"Riepilogo entrate e uscite per ciascun mese del {year_selected}",
    )
    st.plotly_chart(fig, use_container_width=True)

    # USCITE PER MESE, PER CATEGORIA
    df_filtered = df.loc[
        (df["type"] == "Expense") & (df["date"].dt.year == year_selected)
    ]
    df_filtered["month_name"] = df_filtered["date"].dt.strftime("%b")
    df_grouped = (
        df_filtered.groupby(["month_name", "category"])["amount"].sum().reset_index()
    )
    fig = px.bar(
        data_frame=df_grouped,
        x="month_name",
        y="amount",
        color="category",
        barmode="group",
        labels={
            "amount": "Totale spese",
            "month_name": "Mese",
            "category": "categorie",
        },
        title=f"Totale spese per categoria per ciascun mese del {year_selected}",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ENTRATE PER MESE, PER CATEGORIA
    df_filtered = df.loc[
        (df["type"] == "\U0001F4B2 Income") & (df["date"].dt.year == year_selected)
    ]
    df_filtered["month_name"] = df_filtered["date"].dt.strftime("%b")
    df_grouped = (
        df_filtered.groupby(["month_name", "category"])["amount"].sum().reset_index()
    )
    fig = px.bar(
        data_frame=df_grouped,
        x="month_name",
        y="amount",
        color="category",
        barmode="group",
        labels={
            "amount": "Totale entrate",
            "month_name": "Mese",
            "category": "categorie",
        },
        title=f"Totale entrate per categoria per ciascun mese del {year_selected}",
    )
    st.plotly_chart(fig, use_container_width=True)

    category_selected = st.selectbox(
        label="Seleziona la categoria di cui visualizzare le statistiche",
        options=df["category"].unique(),
    )
    # ENTRATE E USCITE PER MESE, PER SOTTOCATEGORIA
    df_filtered = df.loc[
        (df["date"].dt.year == year_selected) & (df["category"] == category_selected)
    ]
    df_filtered["month_name"] = df_filtered["date"].dt.strftime("%b")
    df_grouped = (
        df_filtered.groupby(["month_name", "sub_category"])["amount"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        data_frame=df_grouped,
        x="month_name",
        y="amount",
        color="sub_category",
        barmode="group",
        labels={
            "amount": "Totale spese",
            "month_name": "Mese",
            "sub_category": "sottocategorie",
        },
        title=f"Totale per ciascun mese del {year_selected} della categoria {category_selected}",
    )
    st.plotly_chart(fig, use_container_width=True)

elif range_time_selected == "Annuale":

    # ENTRATE E USCITE PER ANNO
    df_filtered = df.loc[(df["type"].isin(["Expense", "\U0001F4B2 Income"]))]

    df_filtered["year"] = df_filtered["date"].dt.year
    df_grouped = df_filtered.groupby(["year", "type"])["amount"].sum().reset_index()
    df_grouped["year"] = df_grouped["year"].astype(str)
    fig = px.bar(
        data_frame=df_grouped,
        x="year",
        y="amount",
        color="type",
        barmode="group",
        labels={"amount": "Totale spese", "year": "Anno", "type": "Entrate o uscite"},
        title=f"Riepilogo entrate e uscite per ciascun anno",
    )
    fig.update_xaxes(dtick="Y1", tickformat="%Y",ticklabelmode="period")
    st.plotly_chart(fig, use_container_width=True)

    # USCITE PER ANNO
    df_filtered = df.loc[(df["type"] == "Expense")]

    df_filtered["year"] = df_filtered["date"].dt.year
    df_grouped = df_filtered.groupby(["year", "category"])["amount"].sum().reset_index()
    df_grouped["year"] = df_grouped["year"].astype(str)
    fig = px.bar(
        data_frame=df_grouped,
        x="year",
        y="amount",
        color="category",
        barmode="group",
        labels={"amount": "Totale spese", "year": "Anno", "category": "Categoria"},
        title=f"Riepilogo uscite per categoria",
    )
    fig.update_xaxes(dtick="Y1", tickformat="%Y",ticklabelmode="period")
    st.plotly_chart(fig, use_container_width=True)

    # USCITE PER ANNO
    df_filtered = df.loc[(df["type"] == "\U0001F4B2 Income")]

    df_filtered["year"] = df_filtered["date"].dt.year
    df_grouped = df_filtered.groupby(["year", "category"])["amount"].sum().reset_index()
    df_grouped["year"] = df_grouped["year"].astype(str)
    fig = px.bar(
        data_frame=df_grouped,
        x="year",
        y="amount",
        color="category",
        barmode="group",
        labels={"amount": "Totale spese", "year": "Anno", "category": "Categoria"},
        title=f"Riepilogo entrate per categoria",
    )
    fig.update_xaxes(dtick="Y1", tickformat="%Y",ticklabelmode="period")
    st.plotly_chart(fig, use_container_width=True)

    category_selected = st.selectbox(
        label="Seleziona la categoria di cui visualizzare le statistiche",
        options=df["category"].unique(),
    )
