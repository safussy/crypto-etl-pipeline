
import sqlite3
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def load_coingecko_data(records, db_path):

    if not records:
        raise ValueError("No records to load.")

    conn = None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ==================================
        # TABLE 1: LATEST CRYPTOCURRENCY DATA
        # ==================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                coin_id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                name TEXT,
                price_usd REAL NOT NULL,
                market_cap REAL,
                market_cap_rank INTEGER,
                total_volume_usd REAL,
                price_change_24h_pct REAL,
                last_updated_utc TEXT
            );
        """)

        # ==================================
        # TABLE 2: HISTORICAL PRICE SNAPSHOTS
        # ==================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto_price_history (
                snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                name TEXT,
                price_usd REAL NOT NULL,
                market_cap REAL,
                market_cap_rank INTEGER,
                total_volume_usd REAL,
                price_change_24h_pct REAL,
                last_updated_utc TEXT,
                recorded_at TEXT NOT NULL
            );
        """)

        # Index for faster historical queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_coin_time
            ON crypto_price_history (coin_id, recorded_at);
        """)

        # ==================================
        # INSERT OR UPDATE LATEST DATA
        # ==================================

        insert_query = """
            INSERT INTO crypto_prices (
                coin_id, symbol, name, price_usd,
                market_cap, market_cap_rank,
                total_volume_usd, price_change_24h_pct,
                last_updated_utc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(coin_id) DO UPDATE SET
                symbol = excluded.symbol,
                name = excluded.name,
                price_usd = excluded.price_usd,
                market_cap = excluded.market_cap,
                market_cap_rank = excluded.market_cap_rank,
                total_volume_usd = excluded.total_volume_usd,
                price_change_24h_pct = excluded.price_change_24h_pct,
                last_updated_utc = excluded.last_updated_utc;
        """

        cursor.executemany(insert_query, records)

        # ==================================
        # INSERT HISTORICAL SNAPSHOTS
        # ==================================

        # One collection timestamp for this entire batch
        recorded_at = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        history_query = """
            INSERT INTO crypto_price_history (
                coin_id, symbol, name, price_usd,
                market_cap, market_cap_rank,
                total_volume_usd, price_change_24h_pct,
                last_updated_utc, recorded_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        history_records = [
            (*record, recorded_at)
            for record in records
        ]

        cursor.executemany(history_query, history_records)

        # ==================================
        # COMMIT BOTH OPERATIONS
        # ==================================

        conn.commit()

        logger.info(
            f"Successfully updated {len(records)} latest records."
        )

        logger.info(
            f"Successfully stored {len(history_records)} historical snapshots."
        )

        print(f"Latest records updated: {len(records)}")
        print(f"Historical snapshots stored: {len(history_records)}")

    except Exception:

        if conn:
            conn.rollback()

        logger.exception("Database loading failed.")
        raise

    finally:

        if conn:
            conn.close()

