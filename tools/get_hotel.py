# tools/get_hotel.py

import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)


# ===============================
# HÀM TÁCH GIÁ TỪ TEXT
# ===============================
def extract_min_price(price_text):
    try:
        if pd.isna(price_text):
            return None

        # bỏ dấu chấm (900.000 → 900000)
        clean_text = str(price_text).replace(".", "")

        # tách theo dấu -
        parts = clean_text.split("-")

        # lấy phần giá thấp nhất
        min_price = parts[0].strip()

        return float(min_price)

    except:
        return None


# ===============================
# HOTEL TOOL (ĐỘC LẬP)
# ===============================
def get_hotel(location=None, max_price=None) -> pd.DataFrame:

    # ===============================
    # QUERY HOTEL
    # ===============================
    if location:
        query = text("""
            SELECT name, address, price_mean
            FROM hotel
            WHERE address ILIKE :loc
        """)
        df_hotel = pd.read_sql(
            query,
            engine,
            params={"loc": f"%{location}%"}
        )
    else:
        query = text("""
            SELECT name, address, price_mean
            FROM hotel
        """)
        df_hotel = pd.read_sql(query, engine)

    if df_hotel.empty:
        return pd.DataFrame(columns=["name", "address", "price_mean"])

    # ===============================
    # PARSE GIÁ
    # ===============================
    df_hotel["price_numeric"] = df_hotel["price_mean"].apply(extract_min_price)

    # ===============================
    # FILTER THEO MAX_PRICE
    # ===============================
    if max_price is not None:
        try:
            max_price = float(max_price)
        except:
            max_price = None

        if max_price is not None:

            df_filtered = df_hotel[
                df_hotel["price_numeric"] <= max_price
            ]

            if not df_filtered.empty:
                df_hotel = df_filtered
            else:
                # Không có hotel đúng giá → gợi ý gần nhất
                df_hotel["price_diff"] = abs(
                    df_hotel["price_numeric"] - max_price
                )
                df_hotel = df_hotel.sort_values("price_diff")

    # ===============================
    # SORT THEO GIÁ
    # ===============================
    df_hotel = df_hotel.sort_values("price_numeric")

    # ===============================
    # RETURN TOP 5
    # ===============================
    return df_hotel.head(5)[
        ["name", "address", "price_mean"]
    ]