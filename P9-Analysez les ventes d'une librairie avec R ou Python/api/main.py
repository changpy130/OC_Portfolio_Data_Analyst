from fastapi import FastAPI
import sqlite3

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "lapage.db")

app = FastAPI(
    title="API Lapage",
    description="API REST pour les données de la librairie Lapage",
    version="1.0.0"
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows accessing columns by name
    return conn

# region APIs

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API Lapage"}

@app.get("/api/kpis", tags=["KPIs"], summary="Indicateurs clés de performance")
def get_kpis(segment: str = None, sex: str = None):
    """
    Retourne les KPIs globaux :
    - CA total
    - Nombre de clients uniques
    - Nombre de transactions
    - Panier moyen par session
    """
    conn = get_db()

    conditions = []
    param = []

    if segment:
        conditions.append("segment_client = ?")
        param.append(segment)
    if sex:
        conditions.append("sex = ?")
        param.append(sex)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    ca = conn.execute(
        f"SELECT ROUND(SUM(price), 2) as total FROM transactions {where}",
        param
    ).fetchone()

    clients = conn.execute(
        f"SELECT COUNT(DISTINCT client_id) as nb FROM transactions {where}",
        param
    ).fetchone()

    transactions = conn.execute(
        f"SELECT COUNT(*) as nb FROM transactions {where}",
        param
    ).fetchone()

    panier = conn.execute(
        f"""
        SELECT ROUND(AVG(session_total), 2) as moyenne
        FROM (
            SELECT session_id, SUM(price) as session_total
            FROM transactions {where}
            GROUP BY session_id
        )
        """,
        param
    ).fetchone()

    conn.close()

    return {
        "ca_total": ca['total'],
        "nb_clients": clients['nb'],
        "transactions": transactions['nb'],
        "panier_moyen": panier['moyenne'],
        "filters": {
            "segment": segment,
            "sex": sex
        }
    }