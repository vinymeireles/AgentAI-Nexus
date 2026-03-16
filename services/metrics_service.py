# services/metrics_service.py

from services.db import get_conn
from datetime import datetime, timedelta
from services.db import get_conn


def get_date_range(period, start_date=None, end_date=None):

    today = datetime.today()

    if period == "Últimos 7 dias":
        return today - timedelta(days=7), today

    if period == "Últimos 30 dias":
        return today - timedelta(days=30), today

    if period == "Este mês":
        return today.replace(day=1), today

    if period == "Este ano":
        return today.replace(month=1, day=1), today

    if period == "Personalizado" and start_date and end_date:
        return start_date, end_date

    return None, None


def get_metrics(period, segment, product, start_date=None, end_date=None):

    conn = get_conn()
    cursor = conn.cursor()

    start, end = get_date_range(period, start_date, end_date)

    query = """
        SELECT 
            SUM(revenue) as total_revenue,
            COUNT(id) as total_orders,
            SUM(expense) as total_expense
        FROM sales
        WHERE 1=1
    """

    params = []

    # filtro período
    if start and end:
        query += " AND order_date BETWEEN ? AND ?"
        params.append(start.strftime("%Y-%m-%d"))
        params.append(end.strftime("%Y-%m-%d"))

    # filtro produto
    if product and product != "Todos":
        query += " AND product = ?"
        params.append(product)

    # filtro segmento
    if segment and segment != "Todos":
        query += " AND segment = ?"
        params.append(segment)

    cursor.execute(query, params)

    result = cursor.fetchone()
    conn.close()

    return {
        "revenue": result[0] or 0,
        "orders": result[1] or 0,
        "expenses": result[2] or 0,
        "period": period
    }


