import sqlite3
from pathlib import Path

DB_PATH = "crypto_vault.db"
SQL_PATH = "queries/momentum_metrics.sql"

def run_momentum_metrics():
    query = Path(SQL_PATH).read_text(encoding="utf-8")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(query)
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        
        print("\n========== DAY 18: PRICE MOMENTUM & MOVING AVERAGES ==========\n")
        if not results:
            print("No records found.")
        else:
            for row in results:
                print(dict(zip(columns, row)))
                
        print("\nTotal rows analyzed:", len(results))

if __name__ == "__main__":
    run_momentum_metrics()