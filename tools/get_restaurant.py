# tools/get_restaurant.py
"""
Professional restaurant search tool with advanced filtering and matching
"""

import pandas as pd
from sqlalchemy import text
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from utils import safe_db_query, search_by_location, search_by_category, search_by_name, get_top_results

def get_restaurant(
    location: str = None,
    category: str = None,
    name: str = None,
    limit: int = 10
) -> pd.DataFrame:
    """
    Advanced restaurant search with multiple filter options

    Args:
        location: Location filter (e.g., "Quy Nhơn", "Phú Yên")
        category: Category filter (e.g., "hải sản", "Việt Nam", "seafood", "Vietnamese")
        name: Name filter for specific restaurant
        limit: Maximum number of results to return

    Returns:
        DataFrame with restaurant information
    """

    # Query restaurant data
    query = text("""
        SELECT name, address, category, description
        FROM restaurant
    """)

    df = safe_db_query(query)

    if df.empty:
        return pd.DataFrame(columns=["name", "address", "category", "description"])

    # Apply filters in sequence
    if name:
        df = search_by_name(df, name)

    if category:
        df = search_by_category(df, category)

    if location:
        df = search_by_location(df, location)

    # Get top results
    df = get_top_results(df, limit)

    return df[["name", "address", "category", "description"]]