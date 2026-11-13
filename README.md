# Cryptocurrency ETL Pipeline

A python-based ETL pipeline that extracts cryptocurrency market data from the CoinGecko API, transforms and validates the data, and stores historical price snapshots in a SQLite database for SQL-based analysis.

## 1. Project Overview

This project implements an end-to-end data engineering workflow for collecting, processing, storing, and analyzing cryptocurrency market data.

The pipeline retrieves market information for multiple cryptocurrencies, cleans and standardizes the extracted records, and loads them into a relational SQLite database.

It also provides SQL analytics to explore price trends, historical snapshots, moving averages, and market metrics.

## 2. Project Objectives

- Build an automated ETL pipeline using python.
- Extract cryptocurrency market data through a REST API.
- Clean and transform raw JSON data using Pandas.
- Design and manage a SQLite database.
- Maintain historical price snapshots.
- Perform analytical queries using SQL.
- Validate data quality and test pipeline components.
- Measure query performance and explore database indexing.

## 3. Technologies Used

- **python:** Core programming language used to implement the ETL pipeline.
- **CoinGecko API:** REST API used to retrieve cryptocurrency market data.
- **Pandas:** Used for data cleaning, transformation, and preparation.
- **SQLite:** Relational database used to store current and historical cryptocurrency records.
- **SQL:** Used for data aggregation, historical analysis, window functions, and CTEs.
- **Pytest:** Used to test transformation logic and database query correctness.
- **Git & GitHub:** Used for version control and project hosting.
## 4. Architecture and ETL Workflow

The pipeline follows three main ETL stages:

**Extract → Transform → Load**

1. **Extraction:** Retrieve cryptocurrency market data from the CoinGecko API and save raw JSON files.
2. **Transformation:** Clean records, convert data types, handle missing values, and remove duplicates.
3. **Loading:** Insert processed records into SQLite, updating the latest records and storing historical snapshots.
4. **Validation:** Check data completeness, positive prices, and duplicate records.
5. **Analytics:** Execute SQL queries to analyze historical prices and market trends.

### Architecture Flow
```text
CoinGecko API
     |
     v
 extract.py
     |
     v
 transform.py
     |
     v
   load.py
     |
     v
crypto_vault.db
     |
     v
validate.py
```

## 5. Project Structure
```text
crypto-etl-pipeline/
│
├── queries/
│   ├── aggregations.sql
│   ├── check_snapshots.sql
│   ├── latest_snapshot.sql
│   ├── momentum_metrics.sql
│   └── top_assets_cte.sql
│
├── extract.py
├── transform.py
├── load.py
├── validate.py
├── main.py
├── run_aggregations.py
├── run_benchmark.py
├── run_cte.py
├── run_latest_snapshot.py
├── run_momentum.py
├── test_transform.py
├── test_perf.py
├── requirements.txt
├── .gitignore
├── schema.sql
├── init_db.py
├── check_db.py
├── check_volume.py
└── README.md
```
## 6. Database Schema Design

The pipeline uses SQLite to store current cryptocurrency information and historical price snapshots.

### `crypto_prices`

Stores the latest available record for each cryptocurrency.

### `crypto_price_history`

Stores historical snapshots collected during each pipeline execution.

Each new extraction adds historical records instead of replacing previous snapshots.

An index on `(coin_id, recorded_at)` supports queries that filter or order historical records by cryptocurrency and recording time.

## 7. Installation and Setup

### Prerequisites

- python 3.10 or later
- Git
- Internet connection for API extraction

### Clone the repository
```bash
git clone https://github.com/safussy/crypto-etl-pipeline.git
cd crypto-etl-pipeline
```
### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 8. Running the Pipeline

Execute the complete ETL workflow:

```bash
python main.py
```

The pipeline performs extraction, transformation, database loading, and post-load validation.

The SQLite database is stored locally as:

```text
crypto_vault.db
```

Run the pipeline again to collect another historical snapshot.

## 9. SQL Analytics

The project uses SQL queries to analyze cryptocurrency market data and historical price movements.

The main analytical operations include:

- **Historical Aggregations:** Calculate average, minimum, and maximum prices, as well as the total number of recorded snapshots using aggregate functions and `GROUP BY`.
- **Latest Market Snapshot:** Retrieve the most recent market data for each cryptocurrency using subqueries and `MAX()`.
- **Price Momentum:** Analyze price changes between consecutive snapshots using the `LAG()` window function.
- **Moving Averages:** Calculate average prices over a sequence of historical records using window functions.
- **Top Asset Analysis:** Organize and analyze cryptocurrency data using Common Table Expressions (CTEs).

These queries demonstrate how SQL can be used to extract meaningful insights from historical cryptocurrency data.

Run the analytical scripts:

```bash
python run_aggregations.py
python run_latest_snapshot.py
python run_momentum.py
python run_cte.py
```

Query results are displayed in the terminal.
## 10. SQL Query Results

The following examples illustrate the results produced by the project's analytical SQL queries.

### Historical Price Aggregations

The aggregation query calculates average, minimum, and maximum prices across historical snapshots.

| Cryptocurrency | Average Price (USD) | Minimum Price (USD) | Maximum Price (USD) | Snapshots |
|---|---:|---:|---:|---:|
| Bitcoin (BTC) | 69,357.33 | 69,260.00 | 69,434.00 | 3 |
| Ethereum (ETH) | 1,960.48 | 1,959.26 | 1,961.21 | 3 |
| Solana (SOL) | 80.71 | 80.65 | 80.75 | 3 |

### Latest Market Snapshot

The latest snapshot query retrieves the most recent recorded prices.

| Cryptocurrency | Latest Price (USD) |
|---|---:|
| Bitcoin (BTC) | 69,260.00 |
| Ethereum (ETH) | 1,960.96 |
| BNB | 641.04 |
| Solana (SOL) | 80.75 |

### Price Momentum and Moving Averages

Window functions calculate price changes between consecutive snapshots and three-record moving averages.

Example: BNB

| Metric | Result |
|---|---:|
| Current Price | $641.04 |
| Previous Price | $639.78 |
| Price Change | +0.20% |
| Three-Snapshot Moving Average | $640.14 |

### Top Asset Analysis Using CTEs

The CTE query organizes the latest cryptocurrency market data by market capitalization rank.

| Rank | Cryptocurrency | Price (USD) |
|---:|---|---:|
| 1 | Bitcoin (BTC) | 69,260.00 |
| 2 | Ethereum (ETH) | 1,960.96 |
| 3 | Tether (USDT) | 0.999266 |
| 4 | BNB | 641.04 |
| 5 | USD Coin (USDC) | 0.999588 |

These results demonstrate the use of SQL aggregation, subqueries, window functions, and Common Table Expressions for cryptocurrency market analysis.



## 11. Testing and Data Validation

The project includes automated tests using Pytest.

Run the test suite:

```bash
python -m pytest -v
```

The tests cover:

- Numeric conversion and invalid values.
- Timestamp parsing.
- Missing price fields.
- Empty input datasets.
- Duplicate and invalid records.
- Database query correctness.

Post-load validation checks:

- Database table population.
- NULL values in important fields.
- Positive cryptocurrency prices.
- Duplicate cryptocurrency identifiers.
- Historical snapshot availability.

## 12. Performance and Optimization

The project explores database query performance and indexing.

An index on `(coin_id, recorded_at)` supports historical data retrieval.

The benchmark scripts and SQLite query execution plans are used to examine query behavior and identify potential optimization opportunities.

## 13. Future Improvements

- Automate periodic ETL execution.
- Add a dashboard for cryptocurrency market trends.
- Expand data quality monitoring.
- Introduce more advanced market analytics.
- Explore PostgreSQL for larger datasets.
- Add automated integration testing.

## Author

Developed as a data engineering portfolio project.

https://github.com/safussy/crypto-etl-pipeline.git