
import sqlite3
import logging

logger = logging.getLogger(__name__)


def run_post_load_validations(db_path="crypto_vault.db"):
    logger.info("Starting post-load validations...")

    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()

        # 1. Check total number of latest records
        cursor.execute("""
            SELECT COUNT(*)
            FROM crypto_prices;
        """)

        row_count = cursor.fetchone()[0]

        logger.info(f"Database contains {row_count} crypto records.")

        if row_count == 0:
            raise AssertionError("Database table is empty!")

        # 2. Check NULL values
        cursor.execute("""
            SELECT COUNT(*)
            FROM crypto_prices
            WHERE coin_id IS NULL
               OR symbol IS NULL
               OR price_usd IS NULL
               OR last_updated_utc IS NULL;
        """)

        null_records = cursor.fetchone()[0]

        if null_records > 0:
            raise AssertionError(
                f"Found {null_records} records with NULL values."
            )

        # 3. Check invalid prices
        cursor.execute("""
            SELECT COUNT(*)
            FROM crypto_prices
            WHERE price_usd <= 0;
        """)

        invalid_prices = cursor.fetchone()[0]

        if invalid_prices > 0:
            raise AssertionError(
                f"Found {invalid_prices} invalid prices."
            )

        # 4. Check duplicate identifiers
        cursor.execute("""
            SELECT coin_id, COUNT(*)
            FROM crypto_prices
            GROUP BY coin_id
            HAVING COUNT(*) > 1;
        """)

        duplicates = cursor.fetchall()

        if duplicates:
            raise AssertionError(
                f"Duplicate records found: {duplicates}"
            )

        # 5. Check historical snapshots
        cursor.execute("""
            SELECT COUNT(*)
            FROM crypto_price_history;
        """)

        history_count = cursor.fetchone()[0]

        if history_count == 0:
            raise AssertionError("Historical price table is empty!")

        logger.info(
            f"Database contains {history_count} historical snapshots."
        )

        # 6. Check database structure
        cursor.execute("""
            PRAGMA table_info(crypto_prices);
        """)

        columns = [row[1] for row in cursor.fetchall()]

        logger.info(f"Database columns: {columns}")

        logger.info("All post-load validations passed!")

        print("\n========== VALIDATION SUCCESS ==========")
        print(f"Latest records: {row_count}")
        print(f"Historical snapshots: {history_count}")
        print("NULL validation: PASSED")
        print("Price validation: PASSED")
        print("Duplicate validation: PASSED")
        print("========================================\n")

    except Exception:
        logger.exception("Database validation failed.")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    run_post_load_validations()

