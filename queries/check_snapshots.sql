-- sqlite
-- Check the number of historical snapshots per coin

SELECT
    coin_id,
    COUNT(*) AS total_snapshots

FROM crypto_price_history

GROUP BY coin_id

ORDER BY coin_id;