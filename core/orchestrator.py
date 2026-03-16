# core/orchestrator.py

from core.tools.sql_tool import run_sql
from core.llm.llm_config import get_llm
import unicodedata

llm = get_llm()


class OrchestratorAgent:
    # ----------------------------------------------------
    # utils
    # ----------------------------------------------------

    def _normalize(self, text: str):
        text = (text or "").lower().strip()
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
        return " ".join(text.split())

    def _call_llm(self, prompt: str):
        return llm.call(prompt)

    def _rows(self, data):
        if data is None:
            return []

        if isinstance(data, list):
            return [self._normalize_row_keys(r) for r in data if isinstance(r, dict)]

        if isinstance(data, dict):
            return [self._normalize_row_keys(data)]

        if hasattr(data, "to_dict"):
            try:
                rows = data.to_dict(orient="records")
                return [self._normalize_row_keys(r) for r in rows if isinstance(r, dict)]
            except Exception:
                pass

        return []

    def _normalize_row_keys(self, row):
        normalized = {}
        for k, v in row.items():
            normalized[str(k).strip().lower()] = v
        return normalized

    def _get(self, row, *possible_keys, default=None):
        if not isinstance(row, dict):
            return default

        for key in possible_keys:
            key_norm = str(key).strip().lower()
            if key_norm in row:
                return row[key_norm]

        return default

    def _first_value(self, data, *possible_keys, default=0):
        rows = self._rows(data)
        if not rows:
            return default
        return self._get(rows[0], *possible_keys, default=default)

    def _format_brl(self, value):
        try:
            value = float(value or 0)
        except Exception:
            value = 0.0
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _format_int(self, value):
        try:
            return f"{int(value):,}".replace(",", ".")
        except Exception:
            return "0"

    def _format_pct(self, value):
        try:
            return f"{float(value):.2f}%".replace(".", ",")
        except Exception:
            return "0,00%"

    def _safe_lines(self, rows, formatter, empty_message):
        if not rows:
            return empty_message

        lines = []
        for row in rows:
            try:
                line = formatter(row)
                if line:
                    lines.append(line)
            except Exception:
                continue

        if not lines:
            return empty_message

        return "\n".join([f"- {line}" for line in lines])

    def _has_data(self, rows):
        return bool(rows and len(rows) > 0)

    # ----------------------------------------------------
    # intent detection
    # ----------------------------------------------------

    def detect_intent(self, message: str):
        msg = self._normalize(message)

        mapping = {
            "faturamento ultimo mes": "faturamento_mes",
            "comparar jan x fev": "comparar_meses",
            "crescimento ultimos 3 meses": "crescimento",
            "faturamento por estado": "faturamento_estado",
            "mes com maior volume": "mes_volume",
            "receita por forma pagamento": "receita_pagamento",
            "clientes ativos": "clientes_ativos",
            "quantos clientes ativos temos": "clientes_ativos",
            "top 10 clientes": "top_clientes",
            "clientes compra unica": "clientes_compra_unica",
            "clientes inativos 60 dias": "clientes_inativos",
            "clientes inativos +60 dias": "clientes_inativos",
            "clientes por estado": "clientes_estado",
            "produtos mais vendidos": "produtos_vendidos",
            "categorias mais lucrativas": "categorias_lucrativas",
            "produtos sem vendas 30 dias": "produtos_sem_venda",
            "ticket medio geral": "ticket_medio",
            "maior ticket medio": "maior_ticket_medio",
            "taxa de recompra": "taxa_recompra",
            "tendencia de crescimento": "tendencia",
        }

        if msg in mapping:
            return mapping[msg]

        if "clientes ativos" in msg:
            return "clientes_ativos"

        if "faturamento" in msg and "estado" in msg:
            return "faturamento_estado"

        if "produtos mais vendidos" in msg:
            return "produtos_vendidos"

        if "maior ticket medio" in msg:
            return "maior_ticket_medio"

        if "ticket medio" in msg:
            return "ticket_medio"

        if "taxa de recompra" in msg:
            return "taxa_recompra"

        if "faturamento" in msg or "receita" in msg:
            return "faturamento_mes"

        return "general"

    # ----------------------------------------------------
    # main
    # ----------------------------------------------------

    def run(self, user_input: str):
        intent = self.detect_intent(user_input)

        # ---------------------------------------------
        # FATURAMENTO ÚLTIMO MÊS
        # ---------------------------------------------
        if intent == "faturamento_mes":
            sql = """
            SELECT COALESCE(SUM(total_value), 0) AS revenue
            FROM orders
            WHERE order_date >= date_trunc('month', CURRENT_DATE - interval '1 month')
              AND order_date < date_trunc('month', CURRENT_DATE)
            """
            data = run_sql(sql)
            revenue = self._first_value(data, "revenue", default=0)

            if float(revenue or 0) <= 0:
                return "Não encontrei faturamento registrado no último mês."

            return f"O faturamento do último mês foi **{self._format_brl(revenue)}**."

        # ---------------------------------------------
        # FATURAMENTO POR ESTADO
        # ---------------------------------------------
        if intent == "faturamento_estado":
            sql = """
            SELECT
                state,
                COALESCE(SUM(total_value), 0) AS revenue
            FROM orders
            WHERE state IS NOT NULL
              AND TRIM(state) <> ''
            GROUP BY state
            ORDER BY revenue DESC
            LIMIT 5
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'state', default='Estado não informado')} — "
                    f"{self._format_brl(self._get(row, 'revenue', default=0))}"
                ),
                "Não encontrei dados de faturamento por estado."
            )
            return "Estados com maior faturamento:\n\n" + content

        # ---------------------------------------------
        # PRODUTOS MAIS VENDIDOS
        # ---------------------------------------------
        if intent == "produtos_vendidos":
            sql = """
            SELECT
                p.product_name,
                p.category,
                COALESCE(SUM(oi.quantity), 0) AS total_quantity
            FROM order_items oi
            INNER JOIN products p ON p.product_id = oi.product_id
            GROUP BY p.product_name, p.category
            ORDER BY total_quantity DESC, p.product_name ASC
            LIMIT 10
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'product_name', default='Produto sem nome')} "
                    f"({self._get(row, 'category', default='Sem categoria')}) — "
                    f"{self._format_int(self._get(row, 'total_quantity', default=0))} unidades"
                ),
                "Não encontrei dados de produtos mais vendidos."
            )
            return "Produtos mais vendidos:\n\n" + content

        # ---------------------------------------------
        # CATEGORIAS MAIS LUCRATIVAS
        # ---------------------------------------------
        if intent == "categorias_lucrativas":
            sql = """
            SELECT
                COALESCE(p.category, 'Sem categoria') AS category,
                COALESCE(SUM(oi.quantity * oi.price), 0) AS revenue
            FROM order_items oi
            LEFT JOIN products p ON p.product_id = oi.product_id
            GROUP BY COALESCE(p.category, 'Sem categoria')
            ORDER BY revenue DESC
            LIMIT 10
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'category', default='Sem categoria')} — "
                    f"{self._format_brl(self._get(row, 'revenue', default=0))}"
                ),
                "Não encontrei dados das categorias mais lucrativas."
            )
            return "Categorias mais lucrativas:\n\n" + content

        # ---------------------------------------------
        # CLIENTES ATIVOS
        # ---------------------------------------------
        if intent == "clientes_ativos":
            sql = """
            SELECT COUNT(*) AS active_customers
            FROM customers
            WHERE LOWER(TRIM(COALESCE(status, ''))) = 'ativo'
            """
            data = run_sql(sql)
            total = self._first_value(data, "active_customers", default=0)

            if int(total or 0) == 0:
                # fallback por atividade recente
                sql_fallback = """
                SELECT COUNT(DISTINCT customer_id) AS active_customers
                FROM orders
                WHERE order_date >= CURRENT_DATE - interval '90 days'
                """
                data = run_sql(sql_fallback)
                total = self._first_value(data, "active_customers", default=0)

            return f"Temos atualmente **{self._format_int(total)} clientes ativos**."

        # ---------------------------------------------
        # TOP CLIENTES
        # ---------------------------------------------
        if intent == "top_clientes":
            sql = """
            SELECT
                COALESCE(c.name, o.customer_name, 'Cliente sem nome') AS name,
                COUNT(o.id) AS total_orders,
                COALESCE(SUM(o.total_value), 0) AS total_spent
            FROM orders o
            LEFT JOIN customers c ON c.id = o.customer_id
            GROUP BY COALESCE(c.name, o.customer_name, 'Cliente sem nome')
            ORDER BY total_spent DESC, total_orders DESC
            LIMIT 10
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'name', default='Cliente sem nome')} — "
                    f"{self._format_brl(self._get(row, 'total_spent', default=0))} "
                    f"em {self._format_int(self._get(row, 'total_orders', default=0))} pedidos"
                ),
                "Não encontrei dados para montar o top 10 clientes."
            )
            return "Top 10 clientes:\n\n" + content

        # ---------------------------------------------
        # CLIENTES COMPRA ÚNICA
        # ---------------------------------------------
        if intent == "clientes_compra_unica":
            sql = """
            SELECT COUNT(*) AS single_purchase_customers
            FROM (
                SELECT customer_id
                FROM orders
                GROUP BY customer_id
                HAVING COUNT(*) = 1
            ) t
            """
            data = run_sql(sql)
            total = self._first_value(data, "single_purchase_customers", default=0)
            return f"Hoje temos **{self._format_int(total)} clientes com compra única**."

        # ---------------------------------------------
        # CLIENTES INATIVOS
        # ---------------------------------------------
        if intent == "clientes_inativos":
            sql = """
            SELECT COUNT(*) AS inactive_customers
            FROM customers
            WHERE last_order_date IS NOT NULL
              AND last_order_date < CURRENT_DATE - interval '60 days'
            """
            data = run_sql(sql)
            total = self._first_value(data, "inactive_customers", default=0)
            return f"Temos **{self._format_int(total)} clientes inativos há mais de 60 dias**."

        # ---------------------------------------------
        # CLIENTES POR ESTADO
        # ---------------------------------------------
        if intent == "clientes_estado":
            sql = """
            SELECT
                state,
                COUNT(*) AS total_customers
            FROM customers
            WHERE state IS NOT NULL
              AND TRIM(state) <> ''
            GROUP BY state
            ORDER BY total_customers DESC
            LIMIT 10
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'state', default='Estado não informado')} — "
                    f"{self._format_int(self._get(row, 'total_customers', default=0))} clientes"
                ),
                "Não encontrei dados de clientes por estado."
            )
            return "Clientes por estado:\n\n" + content

        # ---------------------------------------------
        # TICKET MÉDIO GERAL
        # ---------------------------------------------
        if intent == "ticket_medio":
            sql = """
            SELECT COALESCE(AVG(total_value), 0) AS avg_ticket
            FROM orders
            """
            data = run_sql(sql)
            ticket = self._first_value(data, "avg_ticket", default=0)

            if float(ticket or 0) <= 0:
                return "Não encontrei dados suficientes para calcular o ticket médio geral."

            return f"O ticket médio geral é **{self._format_brl(ticket)}**."

        # ---------------------------------------------
        # MAIOR TICKET MÉDIO
        # ---------------------------------------------
        if intent == "maior_ticket_medio":
            sql = """
            SELECT
                COALESCE(c.name, MAX(o.customer_name), 'Cliente não identificado') AS customer_name,
                AVG(o.total_value) AS avg_ticket
            FROM orders o
            LEFT JOIN customers c ON c.id = o.customer_id
            GROUP BY o.customer_id, c.name
            ORDER BY avg_ticket DESC
            LIMIT 1
            """
            rows = self._rows(run_sql(sql))

            if not rows:
                return "Não encontrei dados suficientes para calcular o maior ticket médio."

            row = rows[0]
            return (
                f"O maior ticket médio é de **{self._format_brl(self._get(row, 'avg_ticket', default=0))}**, "
                f"pertencente a **{self._get(row, 'customer_name', default='Cliente não identificado')}**."
            )

        # ---------------------------------------------
        # TAXA DE RECOMPRA
        # ---------------------------------------------
        if intent == "taxa_recompra":
            sql = """
            SELECT
                ROUND(
                    100.0 * COUNT(*) FILTER (WHERE total_orders > 1) / NULLIF(COUNT(*), 0),
                    2
                ) AS repurchase_rate
            FROM customers
            """
            data = run_sql(sql)
            rate = self._first_value(data, "repurchase_rate", default=0)
            return f"A taxa de recompra atual é **{self._format_pct(rate)}**."

        # ---------------------------------------------
        # COMPARAR JAN X FEV
        # ---------------------------------------------
        if intent == "comparar_meses":
            sql = """
            SELECT
                EXTRACT(MONTH FROM order_date) AS month_num,
                COALESCE(SUM(total_value), 0) AS revenue
            FROM orders
            WHERE EXTRACT(YEAR FROM order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
              AND EXTRACT(MONTH FROM order_date) IN (1, 2)
            GROUP BY EXTRACT(MONTH FROM order_date)
            ORDER BY month_num
            """
            rows = self._rows(run_sql(sql))

            jan = 0.0
            fev = 0.0

            for row in rows:
                try:
                    month_num = int(self._get(row, "month_num", default=0) or 0)
                except Exception:
                    month_num = 0

                if month_num == 1:
                    jan = float(self._get(row, "revenue", default=0) or 0)
                elif month_num == 2:
                    fev = float(self._get(row, "revenue", default=0) or 0)

            diff = fev - jan
            pct = (diff / jan * 100) if jan > 0 else 0
            direction = "crescimento" if diff >= 0 else "queda"

            return (
                f"Comparando janeiro e fevereiro do ano atual: janeiro teve **{self._format_brl(jan)}** "
                f"e fevereiro teve **{self._format_brl(fev)}**. "
                f"Isso representa um **{direction} de {abs(pct):.2f}%**."
            )

        # ---------------------------------------------
        # RECEITA POR FORMA DE PAGAMENTO
        # ---------------------------------------------
        if intent == "receita_pagamento":
            sql = """
            SELECT
                COALESCE(payment_label, payment_method, 'Não informado') AS payment_type,
                COALESCE(SUM(value), 0) AS revenue
            FROM payments
            GROUP BY COALESCE(payment_label, payment_method, 'Não informado')
            ORDER BY revenue DESC
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'payment_type', default='Não informado')} — "
                    f"{self._format_brl(self._get(row, 'revenue', default=0))}"
                ),
                "Não encontrei dados de receita por forma de pagamento."
            )
            return "Receita por forma de pagamento:\n\n" + content

        # ---------------------------------------------
        # MÊS COM MAIOR VOLUME
        # ---------------------------------------------
        if intent == "mes_volume":
            sql = """
            SELECT
                TO_CHAR(date_trunc('month', order_date), 'YYYY-MM') AS month_ref,
                COUNT(*) AS total_orders,
                COALESCE(SUM(total_value), 0) AS revenue
            FROM orders
            GROUP BY date_trunc('month', order_date)
            ORDER BY total_orders DESC, revenue DESC
            LIMIT 1
            """
            rows = self._rows(run_sql(sql))

            if not rows:
                return "Não encontrei dados suficientes para identificar o mês com maior volume."

            row = rows[0]
            return (
                f"O mês com maior volume foi **{self._get(row, 'month_ref', default='N/D')}**, com "
                f"**{self._format_int(self._get(row, 'total_orders', default=0))} pedidos** e "
                f"**{self._format_brl(self._get(row, 'revenue', default=0))}** em receita."
            )

        # ---------------------------------------------
        # CRESCIMENTO ÚLTIMOS 3 MESES
        # ---------------------------------------------
        if intent == "crescimento":
            sql = """
            SELECT
                TO_CHAR(date_trunc('month', order_date), 'YYYY-MM') AS month_ref,
                COALESCE(SUM(total_value), 0) AS revenue
            FROM orders
            WHERE order_date >= date_trunc('month', CURRENT_DATE) - interval '2 months'
            GROUP BY date_trunc('month', order_date)
            ORDER BY month_ref
            """
            rows = self._rows(run_sql(sql))

            if len(rows) < 2:
                return "Ainda não há dados suficientes para calcular o crescimento dos últimos 3 meses."

            linhas = []
            for row in rows:
                linhas.append(
                    f"{self._get(row, 'month_ref', default='N/D')}: "
                    f"{self._format_brl(self._get(row, 'revenue', default=0))}"
                )

            first = float(self._get(rows[0], "revenue", default=0) or 0)
            last = float(self._get(rows[-1], "revenue", default=0) or 0)
            crescimento = ((last - first) / first * 100) if first > 0 else 0

            return (
                f"Nos últimos 3 meses, a evolução de receita foi: **{' | '.join(linhas)}**. "
                f"No período, houve uma variação de **{crescimento:.2f}%** entre o primeiro e o último mês."
            )

        # ---------------------------------------------
        # PRODUTOS SEM VENDA 30 DIAS
        # ---------------------------------------------
        if intent == "produtos_sem_venda":
            sql = """
            SELECT
                p.product_name,
                p.category
            FROM products p
            WHERE p.product_id NOT IN (
                SELECT DISTINCT oi.product_id
                FROM order_items oi
                INNER JOIN orders o ON o.id = oi.order_id
                WHERE o.order_date >= CURRENT_DATE - interval '30 days'
            )
            ORDER BY p.product_name
            LIMIT 20
            """
            rows = self._rows(run_sql(sql))

            content = self._safe_lines(
                rows,
                lambda row: (
                    f"{self._get(row, 'product_name', default='Produto sem nome')} "
                    f"({self._get(row, 'category', default='Sem categoria')})"
                ),
                "Todos os produtos tiveram vendas nos últimos 30 dias."
            )
            return "Produtos sem vendas nos últimos 30 dias:\n\n" + content

        # ---------------------------------------------
        # TENDÊNCIA
        # ---------------------------------------------
        if intent == "tendencia":
            sql = """
            WITH monthly AS (
                SELECT
                    date_trunc('month', order_date) AS month_ref,
                    COALESCE(SUM(total_value), 0) AS revenue
                FROM orders
                GROUP BY date_trunc('month', order_date)
            ),
            ranked AS (
                SELECT
                    month_ref,
                    revenue,
                    LAG(revenue) OVER (ORDER BY month_ref) AS previous_revenue
                FROM monthly
            )
            SELECT
                TO_CHAR(month_ref, 'YYYY-MM') AS month_ref,
                revenue,
                previous_revenue,
                CASE
                    WHEN previous_revenue IS NULL OR previous_revenue = 0 THEN 0
                    ELSE ROUND(((revenue - previous_revenue) / previous_revenue) * 100, 2)
                END AS growth_pct
            FROM ranked
            ORDER BY month_ref DESC
            LIMIT 1
            """
            rows = self._rows(run_sql(sql))

            if not rows:
                return "Não encontrei dados suficientes para calcular a tendência de crescimento."

            row = rows[0]
            growth = float(self._get(row, "growth_pct", default=0) or 0)
            direction = "alta" if growth >= 0 else "queda"

            return (
                f"A tendência mais recente é de **{direction}**, com variação de "
                f"**{abs(growth):.2f}%** em **{self._get(row, 'month_ref', default='N/D')}** versus o mês anterior."
            )

        # ---------------------------------------------
        # fallback geral
        # ---------------------------------------------
        prompt = f"""
        Você é um analista de CRM e vendas da plataforma AgentAI Nexus.

        Pergunta do usuário:
        {user_input}

        Responda em português do Brasil.
        Seja objetivo, estratégico e profissional.
        Se a pergunta pedir números e eles não estiverem disponíveis, deixe isso explícito.
        Não invente valores.
        """
        return self._call_llm(prompt)