#services/db.py

import sqlite3
from datetime import datetime
import os

DB_PATH = "data/nexus.db"

def get_conn():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        agent_id TEXT,
        insight TEXT,
        pdf_path TEXT,
        created_at TEXT
    )
    """)

    # 🔥 nova tabela de vendas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        segment TEXT,
        revenue REAL,
        expense REAL,
        order_date TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_report(agent_id, insight, pdf_path):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (agent_id, insight, pdf_path, created_at)
        VALUES (?, ?, ?, ?)
    """, (agent_id, insight, pdf_path, datetime.now().strftime("%d/%m/%Y %H:%M")))

    conn.commit()
    conn.close()

def get_reports(agent_id=None):
    conn = get_conn()
    cur = conn.cursor()

    if agent_id:
        cur.execute("SELECT * FROM reports WHERE agent_id=? ORDER BY id DESC", (agent_id,))
    else:
        cur.execute("SELECT * FROM reports ORDER BY id DESC")

    rows = cur.fetchall()
    conn.close()
    return rows
