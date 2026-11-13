
--  PRICE MOMENTUM AND MOVING AVERAGES

WITH price_history AS (

    SELECT
        snapshot_id,
        coin_id,
        symbol,
        name,
        recorded_at,
        price_usd,

        LAG(price_usd) OVER (
            PARTITION BY coin_id
            ORDER BY recorded_at, snapshot_id
        ) AS previous_price

    FROM crypto_price_history
),

momentum AS (

    SELECT
        snapshot_id,
        coin_id,
        symbol,
        name,
        recorded_at,
        price_usd,
        previous_price,

        ROUND(
            (price_usd - previous_price)
            / NULLIF(previous_price, 0) * 100.0,
            2
        ) AS price_change_pct

    FROM price_history
)

SELECT
    snapshot_id,
    coin_id,
    symbol,
    name,
    recorded_at,
    price_usd,
    previous_price,
    price_change_pct,

    CASE
        WHEN COUNT(*) OVER (
            PARTITION BY coin_id
            ORDER BY recorded_at, snapshot_id
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) = 3

        THEN ROUND(
            AVG(price_usd) OVER (
                PARTITION BY coin_id
                ORDER BY recorded_at, snapshot_id
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ),
            2
        )
        ELSE NULL
    END AS moving_avg_3

FROM momentum

ORDER BY coin_id, recorded_at, snapshot_id;

