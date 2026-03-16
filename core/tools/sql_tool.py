# core/tools/sql_tool.py

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Carrega variáveis do .env (sobrescreve existentes)
load_dotenv(override=True)


# ----------------------------------------------------
# Mascara senha para logs seguros
# ----------------------------------------------------
def mask_db_url(db_url: str):
    if not db_url:
        return None

    try:
        prefix, rest = db_url.split("://", 1)
        creds, host_part = rest.split("@", 1)
        user, _password = creds.split(":", 1)
        return f"{prefix}://{user}:*****@{host_part}"
    except Exception:
        return "[URL inválida]"


# ----------------------------------------------------
# Conexão com PostgreSQL (Supabase)
# ----------------------------------------------------
def get_pg_connection():

    db_url = os.getenv("SUPABASE_DB_URL")

    # Conexão via URL completa
    if db_url:
        try:
            return psycopg2.connect(
                db_url,
                cursor_factory=RealDictCursor,
                sslmode="require",
                connect_timeout=10,
                application_name="AgentAI Nexus"
            )
        except Exception as e:
            print("[sql_tool] Falha usando SUPABASE_DB_URL:", e)

    # Fallback usando variáveis separadas
    try:
        return psycopg2.connect(
            host=os.getenv("SUPABASE_DB_HOST"),
            port=os.getenv("SUPABASE_DB_PORT", "5432"),
            dbname=os.getenv("SUPABASE_DB_NAME", "postgres"),
            user=os.getenv("SUPABASE_DB_USER"),
            password=os.getenv("SUPABASE_DB_PASSWORD"),
            cursor_factory=RealDictCursor,
            sslmode="require",
            connect_timeout=10,
            application_name="AgentAI Nexus"
        )
    except Exception as e:
        print("[sql_tool] Falha conexão parâmetros separados:", e)
        raise


# ----------------------------------------------------
# Executa SQL
# ----------------------------------------------------
def run_sql(query: str):

    conn = None
    cur = None

    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute(query)

        # SELECT
        if cur.description is not None:

            rows = cur.fetchall()
            result = [dict(row) for row in rows]

            print(f"[sql_tool] Query executada | {len(result)} linhas")

            return result

        # INSERT / UPDATE / DELETE
        conn.commit()

        print("[sql_tool] Query executada | sem retorno")

        return []

    except Exception as e:

        print(f"""
[sql_tool] ERRO AO EXECUTAR SQL

QUERY:
{query}

ERRO:
{e}
""")

        return []

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()