# Cryptocurrency ETL Pipeline

An end-to-end data engineering project that extracts cryptocurrency market data from the CoinGecko API, transforms and validates it using Python and Pandas, and stores current and historical records in SQLite for SQL-based analysis.

## 1. Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline designed to collect, process, store, and analyze cryptocurrency market data.

The pipeline retrieves market information for multiple cryptocurrencies, cleans and standardizes the extracted data, and loads it into a relational SQLite database.

In addition to data ingestion, the project includes SQL analytical queries for historical aggregations, price momentum, moving averages, and market analysis.

## 2. Project Objectives

- Build an end-to-end ETL pipeline using Python.
- Extract cryptocurrency market data from a REST API.
- Transform raw JSON data using Pandas.
- Handle missing values, invalid records, and duplicates.
- Design and manage a relational SQLite database.
- Maintain historical price snapshots across pipeline executions.
- Perform analytical queries using SQL.
- Implement data quality validation and automated tests.
- Explore database indexing and query performance.

## 3. Technologies Used

- **Python:** Main programming language for the ETL pipeline.
- **CoinGecko API:** External source of cryptocurrency market data.
- **Pandas:** Data cleaning, transformation, and preparation.
- **SQLite:** Relational database for current and historical records.
- **SQL:** Data aggregation, analytical queries, window functions, and CTEs.
- **Pytest:** Automated testing of transformation and database logic.
- **Git & GitHub:** Version control and project hosting.

## 4. System Architecture

The project follows a structured ETL workflow:

**Extract → Transform → Load → Validate → Analyze**

### Architecture Flow

```text
                  CoinGecko API
                        |
                        v
                  1. EXTRACTION
                        |
                        v
                  Raw JSON Files
                        |
                        v
                 2. TRANSFORMATION
                        |
                        v
                   Cleaned Data
                        |
                        v
                     3. LOADING
                        |
                        v
                 SQLite Database
                  /           \
                 v             v
           Latest Data    Historical Data
                 \             /
                  v           v
                  4. VALIDATION
                        |
                        v
                  5. SQL ANALYTICS
                        |
                        v
                   Query Results
```

### Pipeline Components

| Component | Responsibility |
|---|---|
| Extraction | Retrieves market data from CoinGecko and saves raw JSON files. |
| Transformation | Cleans records, converts data types, handles missing values, and removes duplicates. |
| Loading | Updates current records and inserts new historical snapshots into SQLite. |
| Validation | Checks database population, NULL values, positive prices, and duplicate identifiers. |
| Analytics | Executes SQL queries to analyze historical prices and market trends. |

## 5. Project Structure

```text
crypto-etl-pipeline/
│
├── data/
│   └── raw/                      # Raw API responses (local)
│
├── queries/
│   ├── aggregations.sql
│   ├── check_snapshots.sql
│   ├── latest_snapshot.sql
│   ├── momentum_metrics.sql
│   └── top_assets_cte.sql
│
├── extract.py                    # API data extraction
├── transform.py                  # Data cleaning and transformation
├── load.py                       # SQLite database loading
├── validate.py                   # Post-load validation
├── main.py                       # Main ETL orchestration
│
├── run_aggregations.py            # Aggregation query runner
├── run_benchmark.py               # Query performance benchmark
├── run_cte.py                     # CTE query runner
├── run_latest_snapshot.py         # Latest snapshot query runner
├── run_momentum.py                # Momentum analysis runner
│
├── test_transform.py              # Transformation tests
├── test_perf.py                   # Database query test
│
├── schema.sql                     # Database schema reference
├── init_db.py                     # Database initialization utility
├── requirements.txt               # Python dependencies
├── .gitignore
└── README.md
```

## 6. Database Schema Design

The project uses SQLite with two main tables.

### 6.1 `crypto_prices`

Stores the latest available record for each cryptocurrency.

- Uses `coin_id` as the primary key.
- Maintains the latest market information.
- Updates existing records when the pipeline runs again.

### 6.2 `crypto_price_history`

Stores historical market snapshots collected during each ETL execution.

- Maintains multiple records for each cryptocurrency.
- Stores the recording timestamp.
- Preserves previous snapshots instead of overwriting them.

### 6.3 Indexing

An index named `idx_history_coin_time` is created on:

```sql
(coin_id, recorded_at)
```

This supports queries that filter historical records by cryptocurrency and recording time.

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Git.
- Internet connection for API extraction.

### Step 1: Clone the repository

```bash
git clone https://github.com/safussy/crypto-etl-pipeline.git
cd crypto-etl-pipeline
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 8. Running the ETL Pipeline

Execute the complete pipeline:

```bash
python main.py
```

The execution performs:

1. API data extraction.
2. Raw JSON storage.
3. Data transformation.
4. SQLite database loading.
5. Post-load validation.

The database is stored locally in:

```text
crypto_vault.db
```

Run the pipeline again to collect additional historical snapshots.

**Note:** The database and raw API data are generated locally and are not included in the GitHub repository.

## 9. SQL Analytics

The project includes SQL queries covering different analytical operations.

| Analysis | SQL Concepts |
|---|---|
| Historical aggregations | AVG, MIN, MAX, COUNT, GROUP BY |
| Snapshot inspection | Filtering and ordering |
| Latest market snapshot | Subqueries and MAX |
| Price momentum | LAG and window functions |
| Moving averages | Window functions and AVG |
| Top asset analysis | Common Table Expressions (CTEs) |

### Running the analytical queries

```bash
python run_aggregations.py
python run_latest_snapshot.py
python run_momentum.py
python run_cte.py
```

Each script executes its corresponding SQL query against `crypto_vault.db` and displays the results in the terminal.

## 10. Testing and Data Validation

### Automated Testing

The project uses Pytest to verify important pipeline functionality.

Run the tests:

```bash
python -m pytest -v
```

The test suite covers:

- Numeric conversion and invalid values.
- Timestamp parsing.
- Missing price fields.
- Empty input datasets.
- Duplicate and invalid records.
- Database query correctness.

**Latest test result:** 7 tests passed.

### Data Quality Validation

Post-load validation checks:

- Database table population.
- NULL values in important fields.
- Positive cryptocurrency prices.
- Duplicate cryptocurrency identifiers.
- Historical snapshot availability.

## 11. Performance and Optimization

The project includes database query benchmarking and execution-plan inspection.

The historical table uses an index on `(coin_id, recorded_at)` to support historical data retrieval.

The benchmark scripts examine query execution behavior and provide a basis for evaluating possible database optimizations.

Run the benchmark:

```bash
python run_benchmark.py
```

## 12. Future Improvements

- Schedule automatic ETL execution.
- Build a dashboard for cryptocurrency market trends.
- Expand data quality monitoring.
- Add more advanced analytical queries.
- Explore PostgreSQL for larger datasets.
- Introduce automated integration