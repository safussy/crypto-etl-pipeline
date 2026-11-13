# Day 19: Query Optimization & Benchmark Notes

## Execution Plan for `momentum_metrics.sql`

| Selectid | Order | From | Detail |
|---|---|---|---|
| 4 | 0 | 0 | CO-ROUTINE (subquery-4) |
| 6 | 4 | 0 | CO-ROUTINE price_history |
| 9 | 6 | 0 | CO-ROUTINE (subquery-5) |
| 13 | 9 | 224 | SCAN crypto_price_history USING INDEX idx_history_coin_time |
| 38 | 6 | 216 | SCAN (subquery-5) |
| 103 | 4 | 216 | SCAN price_history |
| 133 | 4 | 0 | USE TEMP B-TREE FOR ORDER BY |
| 158 | 0 | 216 | SCAN (subquery-4) |

### Observations
### Observations

- SQLite uses the existing `idx_history_coin_time` index when scanning `crypto_price_history`.
- The index supports data organization by `coin_id` and `recorded_at`, which is useful for the window functions and historical price analysis.
- SQLite still uses a temporary B-tree for an `ORDER BY` operation, indicating that additional sorting is required.
- The query also scans intermediate CTE results (`price_history` and other subqueries) to calculate momentum metrics.
- Since the query analyzes historical snapshots for all coins, scanning the relevant historical records is expected.