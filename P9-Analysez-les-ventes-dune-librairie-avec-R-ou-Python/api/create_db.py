import sqlite3
import pandas as pd

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import load_all_clients

# always resolves relative to this file, not where you run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "lapage.db")

df = load_all_clients()
df["date"] = pd.to_datetime(df["date"])

connection = sqlite3.connect(DB_PATH)
df.to_sql(
    "transactions",
    connection,
    if_exists='replace',
    index=False
)
connection.close()

print(f"✅ DB created with {len(df)} rows")