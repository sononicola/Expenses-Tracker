import streamlit as st


COLUMN_CONFIG = {
"id": "id",
"date": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
"category": "Categoria",
"sub_category": "Sotto categoria",
"comment": "Commento",
"account_name": "Conto",
"type": "Tipologia",
"amount": st.column_config.NumberColumn("Importo", format="%.2f"),
}

st.header("Elenco completo di tutti i movimenti")
st.dataframe(
st.session_state["df"], use_container_width=True, hide_index=True, column_config=COLUMN_CONFIG
)
