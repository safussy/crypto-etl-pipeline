
import sqlite3
import logging

DB_PATH = "crypto_vault.db"
SCHEMA_PATH = "schema.sql"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_database(db_path=DB_PATH):
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()

        with sqlite3.connect(db_path) as connection:
            connection.executescript(schema)

        logger.info("Database initialized successfully: %s", db_path)

    except (sqlite3.Error, OSError) as error:
        logger.error("Database initialization failed: %s", error)
        raise


if __name__ == "__main__":
    initialize_database()
