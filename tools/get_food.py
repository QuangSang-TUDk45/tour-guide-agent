# tools/get_food.py
"""
Professional food search tool with advanced filtering and matching
"""

import pandas as pd
from sqlalchemy import text
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from utils import safe_db_query, search_by_category, search_by_name, get_top_results

def get_food(
    category: str = None,
    tags: str = None,
    name: str = None,
    limit: int = 10
) -> pd.DataFrame:
    """
    Advanced food search with multiple filter options

    Args:
        category: Food category filter (e.g., "món chính", "hải sản", "main dish", "seafood")
        tags: Tags filter for specific food characteristics
        name: Name filter for specific food item
        limit: Maximum number of results to return

    Returns:
        DataFrame with food information
    """

    # Query food data
    query = text("""
        SELECT name, category, tags, description
        FROM food
    """)

    df = safe_db_query(query)

    if df.empty:
        return pd.DataFrame(columns=["name", "category", "tags", "description"])

    # Apply filters in sequence
    if name:
        df = search_by_name(df, name)

    if category:
        df = search_by_category(df, category)

    if tags:
        # Search in tags column
        tags_lower = str(tags).lower()
        df = df[df["tags"].str.lower().str.contains(tags_lower, na=False)]

    # Get top results
    df = get_top_results(df, limit)

    return df[["name", "category", "tags", "description"]]

# Backward compatibility function
def get_food_list(type_of_food: str, filter_tags: str) -> pd.DataFrame:
    """
    Legacy function for backward compatibility
    """
    return get_food(category=type_of_food, tags=filter_tags, limit=5)