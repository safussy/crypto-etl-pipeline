import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def initialize_database(db_path: str = "crypto_vault.db", schema_path: str = "schema.sql"):
    """Reads schema.sql and executes it against the SQLite database."""
    logging.info(f"Initializing database '{db_path}' using '{schema_path}'...")
    
    try:
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_script = f.read()
            
            # Execute multi-statement SQL script
            conn.executescript(schema_script)
            logging.info("Database schema successfully created and initialized.")
            
    except Exception as e:
        logging.critical(f"Failed to initialize database: {e}")
        raise

if __name__ == "__main__":
    initialize_database()