#page/sobre.py

import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_EXEC_PDF = os.path.join(BASE_DIR, "reports", "Relatorio_Executivo.pdf")


def render_sobre():

    # ==================================================
    # HEADER
    # ==================================================
    st.markdown("## Sobre o AgentAI Nexus")
    st.markdown(
        "<span style='color:#6B7280'>Plataforma Inteligente de CRM com Multi-Agentes e Analytics Estratégico</span>",
        unsafe_allow_html=True
    )

    st.divider()

    # ==================================================
    # HERO CARD
    # ==================================================
    st.markdown("""
        <div class="hero-card">
            <div class="hero-header">
                <div class="hero-icon">🚀</div>
                <h3>CRM Inteligente com Agentes de IA</h3>
            </div>
            <p class="hero-desc">
                O <b>AgentAI Nexus</b> conecta seu CRM a uma arquitetura de
                <b>Agentes de Inteligência Artificial</b> que analisam dados em tempo real,
                identificam oportunidades, riscos e tendências estratégicas.
                Mais do que dashboards, o Nexus entrega <b>decisões orientadas por IA</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ==================================================
    # FEATURE CARDS
    # ==================================================
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">🤖</div>
                <div class="agent-title">Arquitetura Multi-Agente</div>
            </div>
            <p class="agent-desc">
                Agentes especializados em Vendas, Clientes, Risco,
                Performance e Inteligência Executiva operando sobre
                o banco SQLite em tempo real.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">📊</div>
                <div class="agent-title">CRM + BI Integrados</div>
            </div>
            <p class="agent-desc">
                Dashboard moderno com métricas estratégicas,
                segmentação de clientes e análise de receita
                por estado, categoria e período.
            </p>
        </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">💬</div>
                <div class="agent-title">Chat CRM Inteligente</div>
            </div>
            <p class="agent-desc">
                Pergunte ao seu banco de dados em linguagem natural
                e receba análises estratégicas geradas por LLM.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">📄</div>
                <div class="agent-title">Relatórios Automatizados</div>
            </div>
            <p class="agent-desc">
                Geração automática de relatórios executivos,
                insights estratégicos e recomendações acionáveis
                para tomada de decisão.
            </p>
        </div>
        """, unsafe_allow_html=True)

    c5, c6 = st.columns(2)

    with c5:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">⚡</div>
                <div class="agent-title">Insights em Tempo Real</div>
            </div>
            <p class="agent-desc">
                Processamento rápido sobre SQLite com análises
                preditivas e identificação automática de padrões.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">🔐</div>
                <div class="agent-title">Estrutura Escalável</div>
            </div>
            <p class="agent-desc">
                Arquitetura preparada para expansão em nuvem,
                integração com APIs externas e múltiplas bases de dados.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ==================================================
    # STACK TECNOLÓGICO
    # ==================================================
    st.divider()

    st.markdown("### Stack Tecnológico")

    st.markdown("""
    <div style="display:flex;flex-wrap:wrap;gap:8px">
        <span class="badge">Python</span>
        <span class="badge">Streamlit</span>
        <span class="badge">SQLite</span>
        <span class="badge">CrewAI</span>
        <span class="badge">LLM</span>
        <span class="badge">Pandas</span>
        <span class="badge">Multi-Agents</span>
        <span class="badge">Business Intelligence</span>
        <span class="badge">Supabase</span>
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # DOCUMENTAÇÃO EXECUTIVA
    # ==================================================
    st.divider()

    st.markdown("### 📘 Documentação Executiva")

    st.markdown("""
    O <b>Relatório Executivo do AgentAI Nexus</b> apresenta a arquitetura,
    modelo multi-agente, estrutura do banco de dados e roadmap estratégico
    da solução. Ideal para gestores e diretores.
    """, unsafe_allow_html=True)

    if os.path.isfile(REPORT_EXEC_PDF):
        with open(REPORT_EXEC_PDF, "rb") as f:
            st.download_button(
                label="📘 Baixar Relatório Executivo (PDF)",
                data=f,
                file_name="Relatorio_Executivo.pdf",
                mime="application/pdf",
                use_container_width=False
        )
    else:
        st.warning("📄 O relatório executivo não disponível.")


    # ==================================================
    # SOBRE A EMPRESA - NexMarket
    # ==================================================
    st.divider()

    st.markdown(" ### Sobre a NexMarket")
    st.image("assets/logo_empresa.png",width=300)
    st.markdown("""
            
    **NexMarket** é uma empresa fundada em **2022** com o objetivo de revolucionar o mercado de vendas de produtos, serviços e relacionamento com clientes.  
    Nossa missão é conectar pessoas e empresas de forma eficiente, oferecendo soluções que facilitem a experiência de compra e potencializem o crescimento de negócios.

    ---
    
    **Quem Somos:**  
    Uma empresa inovadora, focada em unir tecnologia e mercado para simplificar processos de vendas e gestão de clientes, sempre buscando excelência e confiança.

    **Visão:**  
    Ser referência nacional em soluções de mercado, reconhecida pela inovação, qualidade e impacto positivo na experiência dos clientes.

    **Missão:**  
    Facilitar a conexão entre vendedores e clientes, promovendo eficiência, transparência e crescimento para todos os envolvidos.

    **Valores:**  
    - **Inovação:** Buscamos sempre novas soluções que agreguem valor.  
    - **Transparência:** Atuamos com honestidade em todas as nossas relações.  
    - **Excelência:** Entregamos qualidade em cada serviço e solução.  
    - **Sustentabilidade:** Valorizamos práticas que respeitam o meio ambiente.  
    - **Foco no Cliente:** Colocamos o cliente no centro de todas as decisões.

    **Seguimentos de Atuação:**  
    - Comércio de produtos variados (varejo e atacado)  
    - Serviços de atendimento e suporte ao cliente  
    - Consultoria e soluções digitais para otimização de vendas  

    ---
    
    Fundada em 2022, a NexMarket continua crescendo e inovando, consolidando-se como um parceiro confiável para empresas que desejam expandir suas operações e oferecer experiências de alto valor aos clientes.
    """)

# ==================================================
# FOOTER
# ==================================================
st.divider()

st.markdown("""
<div style="text-align:center;color:#6B7280;font-size:14px">
    Projeto desenvolvido por <b>Vinicius Meireles</b><br>
    <b>VIMEUP AI Solutions</b><br>
    Plataforma AgentAI Nexus — CRM Inteligente com Multi-Agentes 2.0
</div>
""", unsafe_allow_html=True)
