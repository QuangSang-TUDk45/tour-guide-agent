#!/usr/bin/env python3
"""
Script to import all Excel data into backup database
"""

import pandas as pd
from sqlalchemy import create_engine
from config import USER, PASSWORD, HOST, PORT

# ==========================================
# DATABASE CONNECTION CONFIGURATION FOR BACKUP
# ==========================================
BACKUP_DB_NAME = "BinhDinh_TourGuide"
BACKUP_DB_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{BACKUP_DB_NAME}"
engine = create_engine(BACKUP_DB_URL)

def import_excel_data():
    """Import data from data_raw.xlsx"""
    print("Importing data from data_raw.xlsx...")

    file_path = r"..\data\data_raw.xlsx"

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

    for sheet_name, config in sheets_config.items():
        table_name = config["table_name"]
        col_mapping = config["columns"]

        try:
            cols_to_read = list(col_mapping.keys())
            df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=cols_to_read)
            df = df.rename(columns=col_mapping)
            df = df.fillna("")
            df = df.astype(str)

            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"✅ Successfully migrated sheet '{sheet_name}' to table '{table_name}'")

        except Exception as e:
            print(f"❌ Error migrating sheet '{sheet_name}': {e}")
            return False

    return True

def import_services_data():
    """Import data from dich_vu.xlsx"""
    print("Importing data from dich_vu.xlsx...")

    file_path = r"..\data\dich_vu.xlsx"
    df = pd.read_excel(file_path)

    df = df.rename(columns={
        "lien_ket_ID_bang_dia_diem": "destination_id",
        "average_price": "price",
        "service_type": "type"
    })

    df = df[["destination_id", "name", "description", "price", "type"]]
    df = df.fillna("")
    df = df.astype(str)

    try:
        df.to_sql("service", engine, if_exists="append", index=False)
        print(f"✅ Successfully imported {len(df)} services")
        return True
    except Exception as e:
        print(f"❌ Error importing services: {e}")
        return False

def import_hotels_data():
    """Import data from khach_san.xlsx"""
    print("Importing data from khach_san.xlsx...")

    file_path = r"..\data\khach_san.xlsx"
    df = pd.read_excel(file_path)

    df = df.rename(columns={
        "Address_new": "address",
        "price_mean": "price",
        "score": "rating",
        "review_count": "review_count"
    })

    df = df[["name", "address", "description", "price", "rating", "review_count"]]
    df = df.fillna("")
    df = df.astype(str)

    try:
        df.to_sql("hotel", engine, if_exists="append", index=False)
        print(f"✅ Successfully imported {len(df)} hotels")
        return True
    except Exception as e:
        print(f"❌ Error importing hotels: {e}")
        return False

def main():
    print("🚀 Starting complete data import to backup database...")
    print(f"Target database: {BACKUP_DB_NAME}")

    tasks = [
        ("Excel Data (restaurant, destination, food)", import_excel_data),
        ("Services Data", import_services_data),
        ("Hotels Data", import_hotels_data)
    ]

    success_count = 0
    for task_name, task_func in tasks:
        print(f"\n{'='*60}")
        print(f"📂 {task_name}")
        print('='*60)

        if task_func():
            success_count += 1
        else:
            print(f"❌ Failed: {task_name}")

    print(f"\n{'='*60}")
    print(f"📊 Import Summary: {success_count}/{len(tasks)} tasks completed successfully")
    print('='*60)

    if success_count == len(tasks):
        print("🎉 All data imported successfully to backup database!")
        print(f"Database: {BACKUP_DB_NAME}")
        print("Tables: restaurant, destination, food, service, hotel")
    else:
        print("⚠️  Some imports failed. Please check the errors above.")

if __name__ == "__main__":
    main()

    if success_count == len(scripts):
        print("✅ All data imported successfully to backup database!")
    else:
        print("⚠️  Some imports failed. Please check the errors above.")

if __name__ == "__main__":
    main()