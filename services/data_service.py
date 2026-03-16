# services/data_service.py

import pandas as pd
from data.database import (
    load_customers,
    load_orders,
    load_products,
    load_order_items,
)


class DataService:
    def __init__(self, context=None):
        self.context = context or {}
        self.customers = load_customers()
        self.orders = load_orders()
        self.products = load_products()
        self.order_items = load_order_items()

    def _prepare_base(self) -> pd.DataFrame:
        customers = self.customers.copy()
        orders = self.orders.copy()
        order_items = self.order_items.copy()
        products = self.products.copy()

        # Datas
        if "order_date" in orders.columns:
            orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
        elif "purchase_timestamp" in orders.columns:
            orders["order_date"] = pd.to_datetime(orders["purchase_timestamp"], errors="coerce")

        # Merge orders + customers
        # Aqui o pandas vai gerar id_order e id_customer
        df = orders.merge(
            customers,
            left_on="customer_id",
            right_on="id",
            how="left",
            suffixes=("_order", "_customer"),
        )

        # Descobrir qual coluna representa o ID do pedido
        order_id_col = None
        for col in ["id_order", "id", "order_id"]:
            if col in df.columns:
                order_id_col = col
                break

        # Merge com itens do pedido
        if not order_items.empty and order_id_col and "order_id" in order_items.columns:
            df = df.merge(
                order_items,
                left_on=order_id_col,
                right_on="order_id",
                how="left",
                suffixes=("", "_item"),
            )

        # Merge com produtos
        if (
            not products.empty
            and "product_id" in df.columns
            and "product_id" in products.columns
        ):
            df = df.merge(
                products,
                on="product_id",
                how="left",
                suffixes=("", "_product"),
            )

        return df

    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        period = self.context.get("period")
        segment = self.context.get("segment")
        product = self.context.get("product")
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")
        state = self.context.get("state")

        today = pd.Timestamp.today().normalize()

        if "order_date" in df.columns:
            if period == "Últimos 7 dias":
                df = df[df["order_date"] >= (today - pd.Timedelta(days=7))]
            elif period == "Últimos 30 dias":
                df = df[df["order_date"] >= (today - pd.Timedelta(days=30))]
            elif period == "Este mês":
                first_day = today.replace(day=1)
                df = df[(df["order_date"] >= first_day) & (df["order_date"] <= today)]
            elif period == "Este ano":
                first_day_year = pd.Timestamp(year=today.year, month=1, day=1)
                df = df[(df["order_date"] >= first_day_year) & (df["order_date"] <= today)]
            elif period == "Personalizado" and start_date and end_date:
                start = pd.to_datetime(start_date, errors="coerce")
                end = pd.to_datetime(end_date, errors="coerce")
                df = df[(df["order_date"] >= start) & (df["order_date"] <= end)]

        if segment and segment != "Todos" and "segment" in df.columns:
            df = df[df["segment"] == segment]

        if product and product != "Todos":
            if "category" in df.columns:
                df = df[df["category"] == product]
            elif "product_category" in df.columns:
                df = df[df["product_category"] == product]

        if state and state != "Todos" and "state" in df.columns:
            df = df[df["state"] == state]

        return df

    def _get_order_id_column(self, df: pd.DataFrame) -> str | None:
        for col in ["id_order", "id", "order_id"]:
            if col in df.columns:
                return col
        return None

    def get_categories(self):
        products = self.products.copy()
        category_col = "category" if "category" in products.columns else None
        if category_col is None:
            return []
        return (
            products[category_col]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

    def get_states(self):
        customers = self.customers.copy()
        if "state" not in customers.columns:
            return []
        return (
            customers["state"]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

    def get_segments(self):
        customers = self.customers.copy()
        if "segment" not in customers.columns:
            return []
        return (
            customers["segment"]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

    def get_kpis(self):
        df = self._apply_filters(self._prepare_base())

        revenue_col = "total_value" if "total_value" in df.columns else None
        revenue = float(df[revenue_col].fillna(0).sum()) if revenue_col else 0.0

        order_id_col = self._get_order_id_column(df)
        orders = int(df[order_id_col].dropna().nunique()) if order_id_col else 0

        return {
            "revenue": revenue,
            "orders": orders,
        }

    def get_customers_count(self):
        df = self._apply_filters(self._prepare_base())
        return int(df["customer_id"].dropna().nunique()) if "customer_id" in df.columns else 0

    def get_active_customers(self):
        df = self._apply_filters(self._prepare_base())
        if "status" in df.columns:
            df = df[df["status"].astype(str).str.lower() == "ativo"]
        return int(df["customer_id"].dropna().nunique()) if "customer_id" in df.columns else 0

    def get_top_states(self, limit=5):
        df = self._apply_filters(self._prepare_base())

        if "state" not in df.columns:
            return pd.DataFrame(columns=["state", "orders", "revenue"])

        revenue_col = "total_value" if "total_value" in df.columns else None
        order_id_col = self._get_order_id_column(df)

        if order_id_col:
            grouped = (
                df.groupby("state", dropna=False)
                .agg(
                    orders=(order_id_col, "nunique"),
                    revenue=(revenue_col, "sum") if revenue_col else (order_id_col, "count"),
                )
                .reset_index()
                .sort_values("revenue", ascending=False)
                .head(limit)
            )
        else:
            grouped = (
                df.groupby("state", dropna=False)
                .size()
                .reset_index(name="orders")
                .sort_values("orders", ascending=False)
                .head(limit)
            )
            grouped["revenue"] = 0

        return grouped

    def execute_dynamic_query(self, sql):
        raise NotImplementedError(
            "execute_dynamic_query foi desativado nesta fase para evitar SQL livre durante a migração para Supabase."
        )