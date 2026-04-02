"""
Tests de l'application Lapage
=============================

3 tests pour valider les fonctionnalités essentielles :
1. Chargement des données
2. Calcul des KPIs
3. Filtrage des données

Exécuter avec : pytest tests/ -v
"""
import pytest
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import load_all_clients

# =============================================================================
# FIXTURES (données partagées entre les tests)
# =============================================================================

@pytest.fixture
def df():
    """Load real data once, shared between all tests."""
    df = load_all_clients()
    df['date'] = pd.to_datetime(df['date'])
    return df


def test_load_data(df):
    """Check that data loads correctly with expected columns and types."""

    # not empty
    assert len(df) > 0, "DataFrame is empty."
    # assert(check) if statement is true, "error message"

    # columns
    expected_cols = ["id_prod", "date", "client_id", "price", "categ", "sex", "age", "segment_client"]
    for col in expected_cols:
        assert col in df.columns, f"Column {col} is missing."

    # types
    assert pd.api.types.is_numeric_dtype(df['price']), "Price column is not numeric."
    assert pd.api.types.is_datetime64_any_dtype(df['date']), "Date column type should be datetime."


def test_kpis(df):
    ca_total = df['price'].sum()
    nb_clients = df['client_id'].nunique()
    nb_transactions = len(df)
    panier_moyen = df['price'].mean()

    assert ca_total > 0, "CA should be more than zero."
    assert panier_moyen > 0, "Average price should be more than zero."

    assert nb_clients <= nb_transactions, "Transactions should be more than clients."

    ca_recalcul = nb_transactions * panier_moyen
    assert abs(ca_total - ca_recalcul) < 0.01, "CA calculation is not consistent."