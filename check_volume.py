
import sqlite3

conn = sqlite3.connect("crypto_vault.db")

query = """
SELECT
    coin_id,
    symbol,
    total_volume_usd,
    recorded_at
FROM crypto_price_history
ORDER BY total_volume_usd DESC;
"""

for row in conn.execute(query):
    print(row)

conn.close()
