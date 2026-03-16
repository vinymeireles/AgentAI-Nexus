# data/database.py

import math
import pandas as pd
import streamlit as st
from services.supabase_client import supabase

PAGE_SIZE = 1000


def _fetch_all_rows(table_name: str) -> list[dict]:
    """
    Busca todos os registros de uma tabela do Supabase em páginas.
    """
    all_rows = []
    start = 0

    while True:
        end = start + PAGE_SIZE - 1
        response = (
            supabase
            .table(table_name)
            .select("*")
            .range(start, end)
            .execute()
        )

        rows = response.data or []
        all_rows.extend(rows)

        if len(rows) < PAGE_SIZE:
            break

        start += PAGE_SIZE

    return all_rows


def _to_dataframe(rows: list[dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


@st.cache_data(ttl=300)
def load_customers():
    rows = _fetch_all_rows("customers")
    return _to_dataframe(rows)


@st.cache_data(ttl=300)
def load_orders():
    rows = _fetch_all_rows("orders")
    return _to_dataframe(rows)


@st.cache_data(ttl=300)
def load_products():
    rows = _fetch_all_rows("products")
    return _to_dataframe(rows)


@st.cache_data(ttl=300)
def load_payments():
    rows = _fetch_all_rows("payments")
    return _to_dataframe(rows)


@st.cache_data(ttl=300)
def load_reviews():
    rows = _fetch_all_rows("reviews")
    return _to_dataframe(rows)


@st.cache_data(ttl=300)
def load_order_items():
    rows = _fetch_all_rows("order_items")
    return _to_dataframe(rows)


@st.cache_data(ttl=300)
def load_states():
    rows = _fetch_all_rows("states")
    return _to_dataframe(rows)


def get_connection():
    """
    Mantido temporariamente apenas para compatibilidade.
    Nesta fase, não usamos mais conexão SQLite aqui.
    """
    return None
