#kpi_tool.py

def get_kpis_summary(data: dict):
    kpis = data["kpis"]

    return {
        "total_revenue": kpis["total_revenue"],
        "total_orders": kpis["total_orders"],
        "total_customers": kpis["total_customers"],
        "active_customers": kpis["active_customers"],
        "cancel_rate": kpis["cancel_rate"],
    }