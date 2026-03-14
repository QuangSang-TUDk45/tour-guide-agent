# tools/utils.py
"""
Utility functions for database tools
"""

import re
import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys

# Add script_init_database to path for config import
script_dir = os.path.join(os.path.dirname(__file__), '..', 'script_init_database')
sys.path.insert(0, script_dir)

try:
    from config import DB_URL
except ImportError:
    # Fallback if config not found
    DB_URL = os.getenv("DB_URL", "postgresql://postgres:admin123@localhost:5432/BinhDinh_TourGuide")

# Initialize database engine
engine = create_engine(DB_URL)

def parse_price_range(price_text: str) -> tuple:
    """
    Parse price text like "500.000 - 1.000.000" or "1.000.000"
    Returns (min_price, max_price) in float, or (None, None) if invalid
    """
    if pd.isna(price_text) or not price_text:
        return None, None

    try:
        # Remove dots and spaces
        clean_text = str(price_text).replace(".", "").replace(" ", "")

        # Handle ranges like "500000-1000000"
        if "-" in clean_text:
            parts = clean_text.split("-")
            min_price = float(parts[0].strip())
            max_price = float(parts[1].strip()) if len(parts) > 1 else min_price
            return min_price, max_price
        else:
            # Single price
            price = float(clean_text)
            return price, price
    except:
        return None, None

def extract_price_numeric(price_text: str) -> float:
    """
    Extract numeric price from text (takes minimum price if range)
    """
    min_price, max_price = parse_price_range(price_text)
    return min_price

def search_by_location(df: pd.DataFrame, location_query: str, location_column: str = "address") -> pd.DataFrame:
    """
    Search dataframe by location using flexible matching
    """
    if not location_query:
        return df

    query_lower = str(location_query).lower().strip()

    # Split query into keywords for better matching
    keywords = query_lower.split()

    def location_match(row):
        address = str(row[location_column]).lower()
        # Check if all keywords are in the address
        return all(keyword in address for keyword in keywords)

    # First try exact keyword match
    matches = df[df.apply(location_match, axis=1)]

    if not matches.empty:
        return matches

    # Fallback: partial match with any keyword
    def partial_match(row):
        address = str(row[location_column]).lower()
        return any(keyword in address for keyword in keywords)

    return df[df.apply(partial_match, axis=1)]

def search_by_category(df: pd.DataFrame, category_query: str, category_column: str = "category") -> pd.DataFrame:
    """
    Search dataframe by category with flexible matching
    """
    if not category_query:
        return df

    query_lower = str(category_query).lower().strip()

    # Direct category mapping for common queries
    category_mappings = {
        "biển": ["beach", "sea", "ocean"],
        "núi": ["mountain", "hill"],
        "đồi": ["hill", "mountain"],
        "rừng": ["forest", "jungle"],
        "thành phố": ["city", "urban"],
        "làng chài": ["fishing village"],
        "đảo": ["island"],
        "suối": ["stream", "waterfall"],
        "hang động": ["cave"],
        "chùa": ["temple", "pagoda"],
        "miếu": ["shrine"],
        "đình": ["communal house"],
        "quán ăn": ["restaurant", "food"],
        "nhà hàng": ["restaurant"],
        "ẩm thực": ["food", "cuisine"],
        "món ăn": ["food", "dish"],
        "đặc sản": ["specialty", "local food"],
        "hải sản": ["seafood"],
        "khách sạn": ["hotel"],
        "nhà nghỉ": ["guesthouse", "hotel"],
        "resort": ["resort"],
        "homestay": ["homestay"],
        "dịch vụ": ["service"],
        "hoạt động": ["activity"],
        "tham quan": ["tour", "visit"],
        "du lịch": ["tourism", "travel"]
    }

    # Find matching categories
    matched_categories = []
    for vietnamese, english_list in category_mappings.items():
        if vietnamese in query_lower:
            matched_categories.extend(english_list)

    # Also check direct English matches
    for eng_cat in category_mappings.values():
        for cat in eng_cat:
            if cat in query_lower:
                matched_categories.append(cat)

    # Remove duplicates
    matched_categories = list(set(matched_categories))

    if matched_categories:
        # Filter by matched categories
        def category_filter(row):
            cat = str(row[category_column]).lower()
            return any(match_cat in cat for match_cat in matched_categories)

        return df[df.apply(category_filter, axis=1)]

    # Fallback: simple string contains
    def simple_match(row):
        cat = str(row[category_column]).lower()
        return query_lower in cat

    return df[df.apply(simple_match, axis=1)]

def search_by_name(df: pd.DataFrame, name_query: str, name_column: str = "name") -> pd.DataFrame:
    """
    Search dataframe by name with flexible matching
    """
    if not name_query:
        return df

    query_lower = str(name_query).lower().strip()

    def name_match(row):
        name = str(row[name_column]).lower()
        # Check if query is substring of name or vice versa
        return query_lower in name or name in query_lower

    return df[df.apply(name_match, axis=1)]

def filter_by_price(df: pd.DataFrame, price_condition: str, price_column: str = "price_numeric") -> pd.DataFrame:
    """
    Filter dataframe by price conditions like "dưới 1 triệu", "trên 500k", "từ 1-2 triệu"
    """
    if not price_condition:
        return df

    condition_lower = str(price_condition).lower()

    # Parse price condition
    min_price = None
    max_price = None

    # Extract numbers from condition
    numbers = re.findall(r'(\d+(?:\.\d+)?)', condition_lower)
    prices = []
    for num in numbers:
        # Convert to float, handle millions
        if "triệu" in condition_lower or "tr" in condition_lower:
            prices.append(float(num) * 1000000)
        elif "k" in condition_lower or "nghìn" in condition_lower:
            prices.append(float(num) * 1000)
        else:
            prices.append(float(num))

    # Determine condition type
    if "dưới" in condition_lower or "ít hơn" in condition_lower or "nhỏ hơn" in condition_lower:
        max_price = prices[0] if prices else None
    elif "trên" in condition_lower or "hơn" in condition_lower or "lớn hơn" in condition_lower:
        min_price = prices[0] if prices else None
    elif "từ" in condition_lower and len(prices) >= 2:
        min_price = prices[0]
        max_price = prices[1]
    elif len(prices) >= 1:
        # Default to max price if just a number
        max_price = prices[0]

    # Apply filters
    if min_price is not None:
        df = df[df[price_column] >= min_price]
    if max_price is not None:
        df = df[df[price_column] <= max_price]

    return df

def get_top_results(df: pd.DataFrame, limit: int = 10, sort_by: str = None) -> pd.DataFrame:
    """
    Get top results, optionally sorted by a column
    """
    if df.empty:
        return df

    if sort_by and sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=True)

    return df.head(limit)

def safe_db_query(query: text, **params) -> pd.DataFrame:
    """
    Safely execute database query with error handling
    """
    try:
        if params:
            return pd.read_sql(query, engine, params=params)
        else:
            return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()