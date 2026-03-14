# tools/get_service.py
"""
Professional service search tool with advanced filtering and matching
"""

import pandas as pd
from sqlalchemy import text
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from utils import safe_db_query, search_by_location, search_by_category, search_by_name, filter_by_price, get_top_results

def get_service(
    location: str = None,
    category: str = None,
    name: str = None,
    price_condition: str = None,
    limit: int = 10
) -> pd.DataFrame:
    """
    Advanced service search with multiple filter options

    Args:
        location: Location filter (e.g., "Eo Gió", "Quy Nhơn")
        category: Service category filter (e.g., "tour", "activity", "ticket")
        name: Name filter for specific service
        price_condition: Price filter (e.g., "dưới 500k", "trên 1 triệu")
        limit: Maximum number of results to return

    Returns:
        DataFrame with service information
    """

    # Query service data with destination info
    query = text("""
        SELECT s.name, s.description, s.price, s.type,
               d.name as destination_name, d.address as destination_address
        FROM service s
        LEFT JOIN destination d ON s.destination_id = d.id
    """)

    df = safe_db_query(query)

    if df.empty:
        return pd.DataFrame(columns=["name", "description", "price", "type", "destination_name", "destination_address"])

    # Add numeric price column for filtering
    df["price_numeric"] = df["price"].apply(lambda x: float(str(x).replace(".", "").replace(",", "")) if str(x).replace(".", "").replace(",", "").isdigit() else None)

    # Apply filters in sequence
    if name:
        df = search_by_name(df, name)

    if category:
        df = search_by_category(df, category, "type")

    if location:
        # Search in destination name or address
        location_lower = str(location).lower()
        df = df[
            df["destination_name"].str.lower().str.contains(location_lower, na=False) |
            df["destination_address"].str.lower().str.contains(location_lower, na=False)
        ]

    if price_condition:
        df = filter_by_price(df, price_condition)

    # Sort by price (lowest first)
    df = df.sort_values("price_numeric", na_position='last')

    # Get top results
    df = get_top_results(df, limit)

    return df[["name", "description", "price", "type", "destination_name", "destination_address"]]

# Backward compatibility function
def get_service_legacy(location: str, filter_tags: str = None):
    """
    Legacy function for backward compatibility - returns dict format
    """
    df = get_service(location=location, name=filter_tags, limit=10)

    if df.empty:
        return {
            "status": "empty",
            "message": "Không tìm thấy dịch vụ phù hợp."
        }

    services = []
    for _, row in df.iterrows():
        services.append({
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "type": row["type"]
        })

    return {
        "status": "success",
        "location": location,
        "services": services
    }