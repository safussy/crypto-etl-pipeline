import json
import logging
import os
from datetime import datetime, timezone
import requests

# 1. Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 2. API endpoint and query parameters
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

HEADERS = {
    "User-Agent": "CryptoETL/1.0 (Data Engineering Educational Project)"
}

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

def fetch_crypto_markets(url: str, params: dict, headers: dict, timeout: int = 10) -> list:
    """
    Sends a GET request to the CoinGecko API to fetch top crypto market snapshots.
    Handles network errors, timeouts, and rate limits gracefully.
    """
    logging.info(f"Initiating GET request to: {url}")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        # Check HTTP status code; raises an HTTPError if status is 4xx or 5xx
        response.raise_for_status()
        
        data = response.json()
        logging.info(f"Extraction successful: received {len(data)} coin records.")
        return data

    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        if response.status_code == 429:
            logging.error("Rate limit reached. CoinGecko public API limits calls per minute.")
        raise
    except requests.exceptions.Timeout:
        logging.error(f"Request timed out after {timeout} seconds.")
        raise
    except requests.exceptions.RequestException as err:
        logging.error(f"Network transport error: {err}")
        raise

def save_raw_landing(records: list, output_dir: str = "data/raw") -> str:
    """
    Persists unparsed payload to disk as an immutable raw landing file.
    """
    os.makedirs(output_dir, exist_ok=True)
    utc_now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"markets_{utc_now}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)
        
    logging.info(f"Raw landing file persisted to: {file_path}")
    return file_path

if __name__ == "__main__":
    try:
        raw_data = fetch_crypto_markets(COINGECKO_BASE_URL, PARAMS, HEADERS)
        saved_path = save_raw_landing(raw_data)
        logging.info("Pipeline Step: Extraction stage completed successfully.")
    except Exception as e:
        logging.critical(f"Pipeline Step: Extraction stage failed: {e}")