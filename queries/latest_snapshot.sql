
-- Latest Snapshot Per Cryptocurrency

WITH ranked_snapshots AS (

    SELECT
        snapshot_id,
        coin_id,
        symbol,
        name,
        price_usd,
        market_cap,
        total_volume_usd,
        recorded_at,

        ROW_NUMBER() OVER (
            PARTITION BY coin_id
            ORDER BY recorded_at DESC, snapshot_id DESC
        ) AS row_num

    FROM crypto_price_history

)

SELECT
    snapshot_id,
    coin_id,
    symbol,
    name,
    price_usd,
    market_cap,
    total_volume_usd,
    recorded_at

FROM ranked_snapshots

WHERE row_num = 1

ORDER BY coin_id;
