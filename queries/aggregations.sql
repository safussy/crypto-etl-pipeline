
--  AGGREGATIONS AND GROUPING
-- CoinGecko Crypto Analytics

SELECT
    coin_id,
    symbol,

    -- Price statistics
    ROUND(AVG(price_usd), 4) AS avg_price_usd,
    ROUND(MIN(price_usd), 4) AS min_price_usd,
    ROUND(MAX(price_usd), 4) AS max_price_usd,

    -- Number of historical observations
    COUNT(*) AS total_snapshots,

    -- Average reported 24-hour trading volume
    ROUND(AVG(total_volume_usd), 2) AS avg_volume_usd

FROM crypto_price_history

-- Keep observations collected during the last 24 hours
WHERE recorded_at >= datetime('now', '-24 hours')

-- Calculate statistics separately for each cryptocurrency
GROUP BY coin_id, symbol

-- Exclude cryptocurrencies with low average trading volume
HAVING AVG(total_volume_usd) >= 100000

-- Display the most active assets first
ORDER BY avg_volume_usd DESC;
