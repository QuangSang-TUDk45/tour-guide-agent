# tools/get_food.py
import pandas as pd
import difflib
import os
import unicodedata
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database connection URL and initialize the SQLAlchemy engine
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def get_food_list(type_of_food: str, filter_tags: str) -> pd.DataFrame:
    """
    Fetches food data from the database, filters it by food category, 
    and returns the top 5 matches based on the similarity of the tags.
    """
    
    # Define a list of valid food categories (in Vietnamese)
    allowed_types = ["món chính", "món phụ", "đồ ăn vặt", "đồ tráng miệng", "đồ uống"]

    # Clean the input food type (lowercase and strip whitespace) to ensure accurate validation
    clean_type = str(type_of_food).lower().strip()
    if clean_type not in allowed_types:
        clean_type = None

    # Construct and execute the SQL query based on whether a valid category was provided
    if clean_type is not None:
        # Parameterized query to fetch data for a specific food category (prevents SQL injection)
        query = text("""
            SELECT name, tags, description 
            FROM food 
            WHERE LOWER(category) = :category
        """)
        # Load the query result into a Pandas DataFrame
        df_filtered = pd.read_sql(query, engine, params={"category": clean_type})
    else:
        # Fallback query to fetch all food items if the category is invalid or not provided
        query = text("SELECT name, tags, description FROM food")
        df_filtered = pd.read_sql(query, engine)

    # Handle the case where the database returns an empty result
    if df_filtered.empty:
        return pd.DataFrame(columns=["name", "description"])

    # Normalize the user's filter tags to lowercase for accurate string comparison
    filter_tags_lower = str(filter_tags).lower()
    sim_scores_list = []

    # Iterate through the 'tags' column to calculate similarity scores
    for tag in df_filtered["tags"]: 
        tag_lower = str(tag).lower()

        # Calculate the string similarity score (returns a float between 0.0 and 1.0)
        score = difflib.SequenceMatcher(None, filter_tags_lower, tag_lower).ratio()

        # Convert the float score to a percentage format with 2 decimals
        score_percentage = round(score * 100, 2)
        sim_scores_list.append(score_percentage)

    # Append the calculated similarity scores as a new column in the DataFrame
    df_filtered["sim_score"] = sim_scores_list
    
    # Extract the top 5 records with the highest similarity scores
    df_result = df_filtered.nlargest(5, 'sim_score').copy()

    # Return only the 'name' and 'description' columns for the final output
    return df_result[["name", "description"]]