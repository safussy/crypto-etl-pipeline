import os
import json
import logging
from datetime import datetime, timezone
import requests

# --- CONFIGURE DUAL LOGGING (Console + pipeline.log) ---
logger = logging.getLogger("crypto_etl")
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_format = logging.Formatter("%(asctime)s [%(levelname)s] [%(filename)s] %(message)s")

    # 1. Terminal Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 2. File Handler (Appends to pipeline.log)
    file_handler = logging.FileHandler("pipeline.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

# Target endpoint settings
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
HEADERS = {"User-Agent": "CryptoETL/1.0 (Educational Data Pipeline)"}
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

def extract_crypto_data(url=COINGECKO_URL, params=PARAMS, headers=HEADERS, timeout=10):
    """Fetches raw market data from CoinGecko with defensive error handling."""
    logger.info(f"Connecting to endpoint: {url}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Extraction successful: retrieved {len(data)} raw coin payloads.")
        return data

    except requests.exceptions.Timeout:
        logger.error(f"Request timed out: server failed to respond within {timeout} seconds.")
        raise
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        if response.status_code == 429:
            logger.error("Rate limit reached: CoinGecko request threshold exceeded.")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Connection failed: check network connectivity or DNS settings.")
        raise
    except requests.exceptions.RequestException as err:
        logger.error(f"Unexpected networking error: {err}")
        raise

def save_raw_payload(data: list, output_dir: str = "data/raw") -> str:
    """Saves raw JSON array into a timestamped file inside data/raw/."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"markets_{timestamp_str}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    logger.info(f"Raw landing file created: {file_path}")
    return file_path

if __name__ == "__main__":
    try:
        raw_records = extract_crypto_data(COINGECKO_URL, PARAMS, HEADERS, timeout=10)
        save_raw_payload(raw_records)
        logger.info("Extraction stage completed successfully.")
    except Exception as e:
        logger.critical(f"Pipeline stopped during extraction: {e}")