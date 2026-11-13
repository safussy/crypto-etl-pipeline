
import sqlite3


def test_query_returns_matching_crypto(tmp_path):

    db_path = tmp_path / "test_crypto.db"

    with sqlite3.connect(db_path) as conn:

        conn.execute("""
            CREATE TABLE crypto_prices (
                coin_id TEXT PRIMARY KEY,
                price_usd REAL,
                last_updated_utc TEXT
            );
        """)

        conn.execute("""
            INSERT INTO crypto_prices
            VALUES ('bitcoin', 68000, '2026-10-28 19:30:00');
        """)

        query = """
            SELECT *
            FROM crypto_prices
            WHERE coin_id = 'bitcoin'
            AND last_updated_utc >= '2026-10-01';
        """

        results = conn.execute(query).fetchall()

        assert len(results) == 1
        assert results[0][0] == "bitcoin"
