import pytest
import pandas as pd
from transform import (
    safe_float,
    safe_int,
    parse_iso_utc,
    transform_single_coin,
    build_cleaned_dataframe,
)

# --- 1. FIXTURES ---

@pytest.fixture
def valid_raw_coin():
    """Provides a valid raw coin record sample."""
    return {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 68500.0,
        "market_cap": 1350000000000.0,
        "market_cap_rank": 1,
        "total_volume": 32000000000.0,
        "price_change_percentage_24h": 2.15,
        "last_updated": "2026-10-28T19:30:00.000Z",
    }


# --- 2. UNIT TESTS: EDGE CASES ---

def test_safe_float_edge_cases():
    """Verifies defensive float conversion across bad/missing inputs."""
    assert safe_float(123.45) == 123.45
    assert safe_float("68500.5") == 68500.5
    assert safe_float("N/A") is None
    assert safe_float(None) is None
    assert safe_float([]) is None


def test_safe_int_edge_cases():
    """Verifies defensive integer conversion across bad/missing inputs."""
    assert safe_int(1) == 1
    assert safe_int("42") == 42
    assert safe_int("invalid") is None
    assert safe_int(None) is None


def test_parse_iso_utc_unexpected_date_strings():
    """Tests timestamp standardization against invalid or malformed strings."""
    # Valid ISO string conversion
    assert parse_iso_utc("2026-10-28T19:30:00.000Z") == "2026-10-28 19:30:00"

    # Malformed / Corrupted date strings
    assert parse_iso_utc("not-a-date") is None
    assert parse_iso_utc("2026/10/28 19:30") is None
    assert parse_iso_utc("") is None
    assert parse_iso_utc(None) is None


def test_transform_single_coin_missing_price_field(valid_raw_coin):
    """Simulates API payload missing price and volume fields."""
    corrupt_coin = valid_raw_coin.copy()
    corrupt_coin["current_price"] = None
    corrupt_coin["total_volume"] = "CorruptedString"

    transformed = transform_single_coin(corrupt_coin)

    # Core metadata preserved
    assert transformed["coin_id"] == "bitcoin"
    # Corrupted / Missing numeric fields gracefully cast to None
    assert transformed["current_price_usd"] is None
    assert transformed["total_volume_usd"] is None


def test_build_cleaned_dataframe_empty_input():
    """Verifies that an empty API response returns an empty DataFrame cleanly."""
    df_empty = build_cleaned_dataframe([])
    assert isinstance(df_empty, pd.DataFrame)
    assert df_empty.empty


def test_build_cleaned_dataframe_deduplication_and_nulls(valid_raw_coin):
    """Tests bulk DataFrame processing on duplicate records and missing coin IDs."""
    duplicate_coin = valid_raw_coin.copy()
    invalid_coin = {"id": None, "symbol": "bad"}  # Should be filtered out

    raw_batch = [valid_raw_coin, duplicate_coin, invalid_coin]
    df = build_cleaned_dataframe(raw_batch)

    # Asserts duplicate 'bitcoin' dropped, invalid coin removed
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["coin_id"] == "bitcoin"