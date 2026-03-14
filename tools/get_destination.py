# tools/get_destination.py
"""
Professional destination search tool with advanced filtering and matching
"""

import pandas as pd
from sqlalchemy import text
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from utils import safe_db_query, search_by_location, search_by_category, search_by_name, get_top_results

def get_destination(
    location: str = None,
    category: str = None,
    name: str = None,
    limit: int = 10
) -> pd.DataFrame:
    """
    Advanced destination search with multiple filter options

    Args:
        location: Location filter (e.g., "Quy Nhơn", "Phú Yên")
        category: Category filter (e.g., "biển", "núi", "beach", "mountain")
        name: Name filter for specific destination
        limit: Maximum number of results to return

    Returns:
        DataFrame with destination information
    """

    # Query destination data
    query = text("""
        SELECT name, category, address, description,
               CAST(gps_lat AS TEXT) as gps_lat,
               CAST(gps_lon AS TEXT) as gps_lon
        FROM destination
    """)

    df = safe_db_query(query)

    if df.empty:
        return pd.DataFrame(columns=["name", "category", "address", "description", "gps_lat", "gps_lon"])

    # Apply filters in sequence
    if name:
        df = search_by_name(df, name)

    if category:
        df = search_by_category(df, category)

    if location:
        df = search_by_location(df, location)

    # Get top results
    df = get_top_results(df, limit)

    return df[["name", "category", "address", "description", "gps_lat", "gps_lon"]]