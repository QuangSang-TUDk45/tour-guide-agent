from sqlalchemy import create_engine, text
import psycopg2

# ==========================================
# DATABASE CONNECTION PARAMETERS
# ==========================================
USER = "postgres"
PASSWORD = "12345" 
HOST = "localhost"
PORT = "5432"
NEW_DB_NAME = "BinhDinh_TourGuide"

# Connection string to the default 'postgres' database for administrative tasks
default_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres"

# Initialize the engine with AUTOCOMMIT to allow database creation commands
engine_default = create_engine(default_url, isolation_level="AUTOCOMMIT")

try:
    with engine_default.connect() as conn:
        # 1. Check if the target database already exists in the system catalog
        check_db_query = text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{NEW_DB_NAME}'")
        db_exists = conn.execute(check_db_query).scalar()

        if not db_exists:
            # 2. Execute the creation command if the database is missing
            # Using double quotes for the database name to handle case sensitivity or special characters
            conn.execute(text(f"CREATE DATABASE \"{NEW_DB_NAME}\""))
            print(f"Successfully created database: {NEW_DB_NAME}")
        else:
            print(f"Database '{NEW_DB_NAME}' already exists. Skipping creation.")

except Exception as e:
    # Log any connection or execution errors
    print(f"Error: {e}")