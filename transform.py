
import os
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

import pandas as pd


# --- CONFIGURE LOGGING ---
logger = logging.getLogger("crypto_etl")
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(
        "pipeline.log", mode="a", encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)


# --- CLEANING HELPERS ---

def parse_iso_utc(timestamp_str: Optional[str]) -> Optional[str]:
    """Convert ISO timestamps to UTC strings."""
    if not timestamp_str or not isinstance(timestamp_str, str):
        return None

    try:
        clean_str = timestamp_str.replace("Z", "+00:00")
        dt_obj = datetime.fromisoformat(clean_str)

        # Treat timestamps without timezone information as UTC
        if dt_obj.tzinfo is None:
            dt_obj = dt_obj.replace(tzinfo=timezone.utc)

        dt_utc = dt_obj.astimezone(timezone.utc)

        return dt_utc.strftime("%Y-%m-%d %H:%M:%S")

    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None


def safe_float(val: Any) -> Optional[float]:
    if val is None:
        return None

    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def safe_int(val: Any) -> Optional[int]:
    if val is None:
        return None

    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def transform_single_coin(coin: Dict[str, Any]) -> Dict[str, Any]:
    """Transform one raw coin record into a flat dictionary."""

    return {
        "coin_id": str(coin.get("id") or "").strip().lower(),
        "symbol": str(coin.get("symbol") or "").strip().upper(),
        "name": str(coin.get("name") or "").strip(),
        "current_price_usd": safe_float(coin.get("current_price")),
        "market_cap": safe_float(coin.get("market_cap")),
        "market_cap_rank": safe_int(coin.get("market_cap_rank")),
        "total_volume_usd": safe_float(coin.get("total_volume")),
        "price_change_24h_pct": safe_float(
            coin.get("price_change_percentage_24h")
        ),
        "last_updated_utc": parse_iso_utc(coin.get("last_updated"))
    }


# --- PANDAS BULK CLEANING ---

def build_cleaned_dataframe(
    raw_records: List[Dict[str, Any]]
) -> pd.DataFrame:

    if not raw_records:
        logger.warning("No records provided.")
        return pd.DataFrame()

    cleaned_dicts = [
        transform_single_coin(coin)
        for coin in raw_records
        if isinstance(coin, dict) and coin.get("id")
    ]

    if not cleaned_dicts:
        raise ValueError("No valid records with cryptocurrency IDs.")

    df = pd.DataFrame(cleaned_dicts)

    initial_count = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=["coin_id"], keep="first")

    # Remove missing and empty identifiers
    df = df.dropna(subset=["coin_id", "symbol"])

    df["coin_id"] = df["coin_id"].str.strip()
    df["symbol"] = df["symbol"].str.strip()

    df = df[
        (df["coin_id"] != "") &
        (df["symbol"] != "")
    ]

    # Remove missing or invalid prices
    df = df.dropna(subset=["current_price_usd"])
    df = df[df["current_price_usd"] > 0]

    # Convert data types
    schema_types = {
        "coin_id": "string",
        "symbol": "string",
        "name": "string",
        "current_price_usd": "float64",
        "market_cap": "float64",
        "market_cap_rank": "Int64",
        "total_volume_usd": "float64",
        "price_change_24h_pct": "float64",
        "last_updated_utc": "string"
    }

    df = df.astype(schema_types)

    rows, cols = df.shape

    logger.info(
        f"Bulk cleaning complete. "
        f"Shape: {rows} rows x {cols} columns. "
        f"Dropped {initial_count - rows} invalid/duplicate rows."
    )

    if df.empty:
        raise ValueError("No valid records after cleaning.")

    return df


# --- LOAD LATEST RAW JSON FILE ---

def load_latest_raw_file(
    raw_dir: str = "data/raw"
) -> List[Dict[str, Any]]:

    if not os.path.isdir(raw_dir):
        raise FileNotFoundError(
            f"Raw data directory '{raw_dir}' does not exist. "
            "Run extract.py first."
        )

    files = [
        os.path.join(raw_dir, f)
        for f in os.listdir(raw_dir)
        if f.endswith(".json")
    ]

    if not files:
        raise FileNotFoundError(
            f"No raw JSON files found in {raw_dir}. Run extract.py first!"
        )

    latest_file = max(files, key=os.path.getmtime)

    logger.info(f"Loading raw file: {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    try:
        raw_data = load_latest_raw_file()
        df_clean = build_cleaned_dataframe(raw_data)

        logger.info(
            f"Successfully transformed {len(df_clean)} records "
            "into validated DataFrame."
        )

    except Exception as e:
        logger.critical(f"Transformation failed: {e}")
        raise
