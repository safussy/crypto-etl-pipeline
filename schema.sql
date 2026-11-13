
-- Current/latest cryptocurrency prices
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

-- Historical cryptocurrency price snapshots
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

-- Index for faster historical queries
CREATE INDEX IF NOT EXISTS idx_history_coin_time
ON crypto_price_history (coin_id, recorded_at);
