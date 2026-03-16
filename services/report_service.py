# services/report_service.py

from datetime import datetime
from utils.pdf import generate_pdf


class ReportService:

    def generate_executive_pdf(self, sales_data, finance_data):
        output_path = "reports/Relatorio_Executivo_Gerado.pdf"

        content = f"""
### Resumo Executivo

#### Contexto
Este relatório apresenta uma visão consolidada dos principais indicadores comerciais e financeiros da operação.

#### Indicadores Comerciais
- Pedidos: **{sales_data['orders']}**
- Receita: **R$ {sales_data['revenue']:,.2f}**
- Insight: **{sales_data['insight']}**

#### Indicadores Financeiros
- Lucro: **R$ {finance_data['profit']:,.2f}**
- Insight: **{finance_data['insight']}**

#### Conclusão
Os resultados reforçam a importância do acompanhamento contínuo dos indicadores para apoiar decisões mais estratégicas e sustentáveis.
        """

        generate_pdf(
            text=content,
            path=output_path,
            title="Relatório Executivo - AgentAI Nexus",
            subtitle="Resumo Comercial e Financeiro"
        )

        return output_path