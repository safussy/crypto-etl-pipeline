import sqlite3
from pathlib import Path

DB_PATH = "crypto_vault.db"
SQL_PATH = "queries/latest_snapshot.sql"

def run_latest_snapshot():
    query = Path(SQL_PATH).read_text(encoding="utf-8")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(query)
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        
        print("\n========== DAY 17: LATEST SNAPSHOT RESULTS ==========\n")
        if not results:
            print("No records found.")
        else:
            for row in results:
                print(dict(zip(columns, row)))
        print("\nTotal assets extracted:", len(results))

if __name__ == "__main__":
    run_latest_snapshot()