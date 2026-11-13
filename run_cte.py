
import sqlite3
from pathlib import Path

DB_PATH = "crypto_vault.db"
SQL_PATH = "queries/top_assets_cte.sql"

def run_cte():

    query = Path(SQL_PATH).read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.execute(query)

        columns = [col[0] for col in cursor.description]

        results = cursor.fetchall()

        print("\n========== DAY 15: CTE RESULTS ==========\n")

        for row in results:
            print(dict(zip(columns, row)))

        print("\nTotal assets selected:", len(results))

if __name__ == "__main__":
    run_cte()
