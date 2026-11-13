
import sqlite3

conn = sqlite3.connect("crypto_vault.db")
cursor = conn.cursor()

# Check database tables
print("\n========== DATABASE TABLES ==========")

tables = cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""").fetchall()

for table in tables:
    print(table[0])

# Check historical records
print("\n========== HISTORICAL SNAPSHOTS ==========")

records = cursor.execute("""
    SELECT
        snapshot_id,
        coin_id,
        price_usd,
        recorded_at
    FROM crypto_price_history;
""").fetchall()

for record in records:
    print(record)

print("\nTotal historical snapshots:", len(records))

conn.close()
