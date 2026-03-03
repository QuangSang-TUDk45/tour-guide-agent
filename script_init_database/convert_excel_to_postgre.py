import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2

# ==========================================
# DATABASE CONNECTION CONFIGURATION
# ==========================================
DB_URL = "postgresql://postgres:12345@localhost:5432/BinhDinh_TourGuide"
engine = create_engine(DB_URL)

# Path to the raw data file
file_path = r"data\data_raw.xlsx"

# ==========================================
# DATA MAPPING CONFIGURATION
# ==========================================
# Mapping Excel sheets and columns to database tables and fields
sheets_config = {
    "nha_hang": {
        "table_name": "restaurant",
        "columns": {
            "Name": "name",
            "address_new": "address",
            "Cuisine": "category",
            "Description": "description"
        }
    },
    "dia_diem": {
        "table_name": "destination",
        "columns": {
            "name": "name",
            "Category": "category",
            "Address_new": "address",
            "describe": "description"
        }
    },
    "am_thuc": {
        "table_name": "food",
        "columns": {
            "ten_mon_an": "name",
            "loai_mon_an": "category",
            "Tags": "tags",
            "Description": "description"
        }
    }
}

# ==========================================
# DATA MIGRATION EXECUTION
# ==========================================
for sheet_name, config in sheets_config.items():
    table_name = config["table_name"]
    col_mapping = config["columns"]
    
    try:
        # 1. Read specific columns from the current Excel sheet
        cols_to_read = list(col_mapping.keys())
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=cols_to_read)
        
        # 2. Rename columns to match the target database schema
        df = df.rename(columns=col_mapping)
        
        # 3. Data Cleaning: Fill missing values and ensure string types
        df = df.fillna("")
        df = df.astype(str)
        
        # 4. Export DataFrame to the PostgreSQL database
        # Note: 'replace' will drop the table if it exists and recreate it
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
        
        print(f"Successfully migrated sheet: '{sheet_name}' to table: '{table_name}'")
        
    except Exception as e:
        # Log any errors encountered during the migration of a specific sheet
        print(f"Error, Sheet name: '{sheet_name}': {e}\n")