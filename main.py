
import time
import logging

from extract import extract_crypto_data, save_raw_payload
from transform import build_cleaned_dataframe
from load import load_coingecko_data
from validate import run_post_load_validations


# --- CONFIGURATION ---
DB_PATH = "crypto_vault.db"


# --- LOGGING ---
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s]: %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():

    start_time = time.perf_counter()

    logger.info("========== ETL PIPELINE STARTED ==========")

    try:

        # STEP 1: EXTRACT
        logger.info("STEP 1: EXTRACT")

        raw_data = extract_crypto_data()

        if not raw_data:
            raise ValueError("No data received from CoinGecko.")

        save_raw_payload(raw_data)

        # STEP 2: TRANSFORM
        logger.info("STEP 2: TRANSFORM")

        clean_df = build_cleaned_dataframe(raw_data)

        if clean_df.empty:
            raise ValueError("Clean DataFrame is empty.")

        logger.info(
            f"Transformed columns: {clean_df.columns.tolist()}"
        )

        print("\nTRANSFORM RESULTS")
        print(clean_df.head())

        # STEP 3: PREPARE RECORDS
        logger.info("STEP 3: PREPARING RECORDS")

        records = [
            (
                row["coin_id"],
                row["symbol"],
                row["name"],
                row["current_price_usd"],
                row["market_cap"],
                row["market_cap_rank"],
                row["total_volume_usd"],
                row["price_change_24h_pct"],
                row["last_updated_utc"]
            )
            for _, row in clean_df.iterrows()
        ]

        # STEP 4: LOAD
        logger.info("STEP 4: LOAD")

        load_coingecko_data(records, DB_PATH)

        # STEP 5: VALIDATE
        logger.info("STEP 5: VALIDATE")

        run_post_load_validations(DB_PATH)

        # FINAL SUMMARY
        duration = time.perf_counter() - start_time

        logger.info("========== ETL PIPELINE SUCCESS ==========")
        logger.info(f"Records processed: {len(records)}")
        logger.info(f"Execution duration: {duration:.2f} seconds")

        print("\n========== ETL PIPELINE SUCCESS ==========")
        print(f"Records processed: {len(records)}")
        print(f"Execution time: {duration:.2f} seconds")
        print(f"Database: {DB_PATH}")
        print("==========================================")

    except Exception:

        logger.exception("ETL PIPELINE FAILED")

        print("\nETL PIPELINE FAILED. Check pipeline.log")

        raise


if __name__ == "__main__":
    run_pipeline()

