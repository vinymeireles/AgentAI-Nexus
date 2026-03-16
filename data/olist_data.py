"""
Olist Ecommerce - Gerador de dados simulados.
Replica exata da logica em lib/olist-data.ts usando NumPy seed(42).
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

BRAZILIAN_STATES: dict[str, str] = {
    "SP": "Sao Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais",
    "BA": "Bahia", "RS": "Rio Grande do Sul", "PR": "Parana",
    "PE": "Pernambuco", "CE": "Ceara", "PA": "Para", "SC": "Santa Catarina",
    "MA": "Maranhao", "GO": "Goias", "AM": "Amazonas", "ES": "Espirito Santo",
    "PB": "Paraiba", "RN": "Rio Grande do Norte", "MT": "Mato Grosso",
    "AL": "Alagoas", "PI": "Piaui", "DF": "Distrito Federal",
    "MS": "Mato Grosso do Sul", "SE": "Sergipe", "RO": "Rondonia",
    "TO": "Tocantins", "AC": "Acre", "AP": "Amapa", "RR": "Roraima",
}

FIRST_NAMES = [
    "Ana", "Pedro", "Maria", "Joao", "Carla", "Lucas", "Fernanda", "Rafael",
    "Juliana", "Bruno", "Patricia", "Diego", "Camila", "Marcos", "Leticia",
    "Felipe", "Amanda", "Thiago", "Vanessa", "Gustavo", "Larissa", "Roberto",
    "Tatiana", "Anderson", "Priscila", "Ricardo", "Beatriz", "Eduardo", "Simone",
    "Gabriel", "Daniela", "Alexandre", "Cristina", "Fernando", "Monica", "Andre",
    "Renata", "Paulo", "Sandra", "Carlos", "Adriana", "Rodrigo", "Isabela",
    "Marcelo", "Helena", "Fabio", "Lucia", "Leonardo", "Rosa", "Vinicius",
]

LAST_NAMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues",
    "Almeida", "Nascimento", "Lima", "Araujo", "Fernandes", "Carvalho", "Gomes",
    "Martins", "Rocha", "Ribeiro", "Barros", "Freitas", "Moreira", "Dias",
    "Nunes", "Vieira", "Monteiro", "Cardoso", "Mendes", "Correia", "Teixeira",
    "Pinto", "Lopes",
]

CITIES: dict[str, list[str]] = {
    "SP": ["Sao Paulo", "Campinas", "Guarulhos", "Osasco", "Santos", "Ribeirao Preto"],
    "RJ": ["Rio de Janeiro", "Niteroi", "Petropolis", "Nova Iguacu", "Duque de Caxias"],
    "MG": ["Belo Horizonte", "Uberlandia", "Contagem", "Juiz de Fora", "Betim"],
    "BA": ["Salvador", "Feira de Santana", "Vitoria da Conquista", "Camacari"],
    "RS": ["Porto Alegre", "Caxias do Sul", "Canoas", "Pelotas", "Santa Maria"],
    "PR": ["Curitiba", "Londrina", "Maringa", "Ponta Grossa", "Cascavel"],
    "PE": ["Recife", "Jaboatao dos Guararapes", "Olinda", "Caruaru"],
    "CE": ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Maracanau"],
    "PA": ["Belem", "Ananindeua", "Santarem", "Maraba"],
    "SC": ["Florianopolis", "Joinville", "Blumenau", "Chapeco"],
    "MA": ["Sao Luis", "Imperatriz", "Timon", "Caxias"],
    "GO": ["Goiania", "Aparecida de Goiania", "Anapolis"],
    "AM": ["Manaus", "Parintins", "Itacoatiara"],
    "ES": ["Vitoria", "Vila Velha", "Serra", "Cariacica"],
    "DF": ["Brasilia", "Taguatinga", "Ceilandia"],
}

PRODUCT_CATEGORIES = [
    "Eletronicos", "Moda Feminina", "Moda Masculina", "Casa e Jardim",
    "Esportes", "Beleza e Saude", "Informatica", "Celulares",
    "Automotivo", "Brinquedos", "Livros", "Alimentos",
    "Ferramentas", "Moveis", "Cama Mesa e Banho",
]

PAYMENT_METHODS = ["credit_card", "boleto", "debit_card", "voucher", "pix"]
PAYMENT_WEIGHTS = [0.45, 0.20, 0.10, 0.05, 0.20]

PAYMENT_LABELS: dict[str, str] = {
    "credit_card": "Cartao de Credito",
    "boleto": "Boleto",
    "debit_card": "Cartao de Debito",
    "voucher": "Voucher",
    "pix": "PIX",
}

ORDER_STATUSES = ["entregue", "enviado", "processando", "cancelado"]

MONTH_NAMES = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez",
]

# Distribuicao ponderada por estado
WEIGHTED_STATES: list[str] = (
    ["SP"] * 30 + ["RJ"] * 18 + ["MG"] * 12 + ["BA"] * 8 +
    ["RS"] * 7 + ["PR"] * 7 + ["PE"] * 5 + ["CE"] * 4 +
    ["SC"] * 3 + ["PA"] * 2 + ["GO"] * 2 + ["DF"] * 2 +
    [s for s in BRAZILIAN_STATES if s not in
     ["SP", "RJ", "MG", "BA", "RS", "PR", "PE", "CE", "SC", "PA", "GO", "DF"]]
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pick(arr: list) -> any:
    return arr[np.random.randint(0, len(arr))]


def _rand(low: float, high: float) -> float:
    return low + np.random.random() * (high - low)


def format_currency(value: float) -> str:
    """Formata valor para Real brasileiro."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(value: int | float) -> str:
    """Formata numero com separadores de milhar."""
    if isinstance(value, float):
        return f"{value:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:,}".replace(",", ".")


# ---------------------------------------------------------------------------
# Geradores
# ---------------------------------------------------------------------------

def generate_customers(count: int = 500) -> pd.DataFrame:
    """Gera DataFrame de clientes simulados."""
    rows = []
    for i in range(count):
        first = _pick(FIRST_NAMES)
        last = _pick(LAST_NAMES)
        state = _pick(WEIGHTED_STATES)
        city_list = CITIES.get(state, [f"Capital de {BRAZILIAN_STATES.get(state, state)}"])
        city = _pick(city_list)
        total_orders = int(_rand(1, 25))
        avg_order = _rand(50, 800)
        total_spent = round(total_orders * avg_order, 2)

        roll = np.random.random()
        status = "ativo" if roll < 0.6 else ("inativo" if roll < 0.85 else "novo")

        seg_roll = np.random.random()
        segment = "premium" if total_spent > 5000 else ("regular" if seg_roll < 0.5 else "ocasional")

        month = int(_rand(1, 13))
        day = int(_rand(1, 29))
        email_num = int(np.random.random() * 99)

        rows.append({
            "id": f"CLT-{i + 1:05d}",
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}{email_num}@email.com",
            "city": city,
            "state": state,
            "zip_code": f"{int(_rand(10000, 99999)):05d}-{int(_rand(100, 999))}",
            "total_orders": total_orders,
            "total_spent": total_spent,
            "last_order_date": f"2024-{month:02d}-{day:02d}",
            "status": status,
            "segment": segment,
        })
    return pd.DataFrame(rows)


def generate_orders(customers_df: pd.DataFrame) -> pd.DataFrame:
    """Gera DataFrame de pedidos a partir dos clientes."""
    rows = []
    idx = 0
    for _, c in customers_df.iterrows():
        n = int(_rand(1, min(c["total_orders"] + 1, 6)))
        for _ in range(n):
            idx += 1
            month = int(_rand(1, 13))
            day = int(_rand(1, 29))

            roll = np.random.random()
            status = (
                "entregue" if roll < 0.65 else
                "enviado" if roll < 0.80 else
                "processando" if roll < 0.92 else
                "cancelado"
            )

            pm = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)
            value = round(_rand(25, 2500), 2)
            delivery_month = min(month + 1, 12)

            rows.append({
                "id": f"ORD-{idx:06d}",
                "customer_id": c["id"],
                "customer_name": c["name"],
                "status": status,
                "order_date": f"2024-{month:02d}-{day:02d}",
                "delivery_date": f"2024-{delivery_month:02d}-{day:02d}" if status == "entregue" else None,
                "total_value": value,
                "payment_method": pm,
                "product_category": _pick(PRODUCT_CATEGORIES),
                "state": c["state"],
                "city": c["city"],
                "review_score": int(_rand(1, 6)) if status == "entregue" else None,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Agregacoes
# ---------------------------------------------------------------------------

def get_kpis(customers_df: pd.DataFrame, orders_df: pd.DataFrame) -> dict:
    total_revenue = orders_df["total_value"].sum()
    total_orders = len(orders_df)
    total_customers = len(customers_df)
    avg_ticket = total_revenue / total_orders if total_orders else 0
    delivered = orders_df[orders_df["status"] == "entregue"]
    avg_review = delivered["review_score"].mean() if len(delivered) else 0
    active_customers = len(customers_df[customers_df["status"] == "ativo"])
    cancelled = len(orders_df[orders_df["status"] == "cancelado"])
    cancel_rate = (cancelled / total_orders * 100) if total_orders else 0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "avg_ticket": round(avg_ticket, 2),
        "avg_review": round(avg_review, 1),
        "active_customers": active_customers,
        "cancel_rate": round(cancel_rate, 1),
        "delivered_orders": len(delivered),
    }


def get_monthly_revenue(orders_df: pd.DataFrame) -> pd.DataFrame:
    month_map = {m: {"revenue": 0.0, "orders": 0} for m in MONTH_NAMES}
    for _, o in orders_df.iterrows():
        m_idx = int(o["order_date"].split("-")[1]) - 1
        key = MONTH_NAMES[m_idx]
        month_map[key]["revenue"] += o["total_value"]
        month_map[key]["orders"] += 1

    rows = [{"month": m, "revenue": round(d["revenue"], 2), "orders": d["orders"]}
            for m, d in month_map.items()]
    return pd.DataFrame(rows)


def get_category_data(orders_df: pd.DataFrame) -> pd.DataFrame:
    cat = orders_df.groupby("product_category").agg(
        revenue=("total_value", "sum"),
        orders=("total_value", "count"),
    ).reset_index()
    cat.columns = ["category", "revenue", "orders"]
    total = cat["revenue"].sum()
    cat["percentage"] = (cat["revenue"] / total * 100).round(1)
    cat["revenue"] = cat["revenue"].round(2)
    return cat.sort_values("revenue", ascending=False).reset_index(drop=True)


def get_payment_data(orders_df: pd.DataFrame) -> pd.DataFrame:
    pm = orders_df["payment_method"].value_counts().reset_index()
    pm.columns = ["method", "count"]
    total = pm["count"].sum()
    pm["label"] = pm["method"].map(PAYMENT_LABELS)
    pm["percentage"] = (pm["count"] / total * 100).round(1)
    return pm.sort_values("count", ascending=False).reset_index(drop=True)


def get_state_data(orders_df: pd.DataFrame) -> pd.DataFrame:
    state_agg = orders_df.groupby("state").agg(
        customers=("customer_id", "nunique"),
        revenue=("total_value", "sum"),
        orders=("total_value", "count"),
    ).reset_index()
    state_agg["avg_ticket"] = (state_agg["revenue"] / state_agg["orders"]).round(2)
    state_agg["revenue"] = state_agg["revenue"].round(2)
    state_agg["state_name"] = state_agg["state"].map(BRAZILIAN_STATES)
    return state_agg.sort_values("revenue", ascending=False).reset_index(drop=True)


def get_order_status_counts(orders_df: pd.DataFrame) -> pd.DataFrame:
    total = len(orders_df)
    counts = orders_df["status"].value_counts().reset_index()
    counts.columns = ["status", "count"]
    counts["percentage"] = (counts["count"] / total * 100).round(1)
    status_order = {"entregue": 0, "enviado": 1, "processando": 2, "cancelado": 3}
    counts["sort_key"] = counts["status"].map(status_order)
    return counts.sort_values("sort_key").drop(columns=["sort_key"]).reset_index(drop=True)


def get_all_states(customers_df: pd.DataFrame) -> list[str]:
    return sorted(customers_df["state"].unique().tolist())


# ---------------------------------------------------------------------------
# Gerar dados (cache-friendly)
# ---------------------------------------------------------------------------

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera e retorna (customers_df, orders_df) com até 5000 registros."""
    
    customers_df = generate_customers(5000)  # 👈 agora 5000 clientes
    orders_df = generate_orders(customers_df)

    return customers_df, orders_df
