# tools/get_hotel.py
"""
Professional hotel search tool with advanced price filtering and location matching
"""

import pandas as pd
from sqlalchemy import text
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from utils import safe_db_query, search_by_location, extract_price_numeric, filter_by_price, get_top_results

def get_hotel(
    location: str = None,
    price_condition: str = None,
    name: str = None,
    limit: int = 10
) -> pd.DataFrame:
    """
    Advanced hotel search with multiple filter options

    Args:
        location: Location filter (e.g., "Quy Nhơn", "Phú Yên")
        price_condition: Price filter (e.g., "dưới 1 triệu", "trên 500k", "từ 1-2 triệu")
        name: Name filter for specific hotel
        limit: Maximum number of results to return

    Returns:
        DataFrame with hotel information
    """

    # Query hotel data - using correct column names
    query = text("""
        SELECT name, address, description, price_mean, gps_lat, gps_lon
        FROM hotel
    """)

    df = safe_db_query(query)

    if df.empty:
        return pd.DataFrame(columns=["name", "address", "description", "price_mean", "gps_lat", "gps_lon"])

    # Rename price_mean to price for consistency
    df = df.rename(columns={"price_mean": "price"})

    # Add numeric price column for filtering
    df["price_numeric"] = df["price"].apply(extract_price_numeric)

    # Apply filters in sequence
    if name:
        # Simple name matching
        name_lower = str(name).lower()
        df = df[df["name"].str.lower().str.contains(name_lower, na=False)]

    if location:
        df = search_by_location(df, location)

    if price_condition:
        df = filter_by_price(df, price_condition)

    # No rating column in database, skip rating filter
    # Sort by price (lowest first) since no rating available
    df = df.sort_values("price_numeric", ascending=True, na_position='last')

    # Get top results
    df = get_top_results(df, limit)

    return df[["name", "address", "description", "price", "gps_lat", "gps_lon"]]