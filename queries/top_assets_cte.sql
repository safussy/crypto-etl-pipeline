--  DEDUPLICATION QUERY
-- Extract the single latest snapshot per asset using Window Functions

WITH RankedSnapshots AS (
    SELECT 
        coin_id,
        symbol,
        name,
        price_usd,
        market_cap,
        market_cap_rank,
        total_volume_usd,
        price_change_24h_pct,
        last_updated_utc,
        recorded_at,
        -- Assign a row number starting at 1 for the newest record per coin
        ROW_NUMBER() OVER (
            PARTITION BY coin_id 
            ORDER BY recorded_at DESC
        ) AS rn
    FROM crypto_price_history
)
SELECT 
    coin_id,
    symbol,
    name,
    price_usd,
    market_cap,
    market_cap_rank,
    total_volume_usd,
    price_change_24h_pct,
    last_updated_utc,
    recorded_at
FROM RankedSnapshots
WHERE rn = 1
ORDER BY market_cap_rank ASC;