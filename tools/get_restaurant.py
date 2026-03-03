# tools/get_restaurant.py
import pandas as pd
import difflib
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database connection URL from environment variables
DB_URL = os.getenv("DB_URL")

# Initialize the SQLAlchemy engine for PostgreSQL connection
engine = create_engine(DB_URL)

def get_restaurant(filter_tags: str) -> pd.DataFrame:
    """
    Fetches restaurant data from the database and returns the top 10 matches
    based on the similarity between the user's filter tags and the restaurant's category.
    """
    
    # Define the SQL query to fetch necessary columns from the 'restaurant' table
    query = text("SELECT name, address, category, description FROM restaurant")
    
    # Execute the query and load the result into a Pandas DataFrame
    df_restaurant = pd.read_sql(query, engine)

    # Handle the case where the database returns an empty result
    if df_restaurant.empty:
        return pd.DataFrame(columns=["name", "address", "description"])

    # Normalize the input filter tags to lowercase for accurate comparison
    filter_tags_lower = str(filter_tags).lower()
    sim_scores_list = []

    # Iterate through each category in the DataFrame to calculate similarity
    for tag in df_restaurant["category"]:
        # Normalize the database category tag to lowercase
        tag_lower = str(tag).lower()

        # Calculate the string similarity score (returns a float between 0.0 and 1.0)
        score = difflib.SequenceMatcher(None, filter_tags_lower, tag_lower).ratio()

        # Convert the float score to a percentage format with 2 decimals (e.g., 85.50)
        score_percentage = round(score * 100, 2)
        sim_scores_list.append(score_percentage)

    # Append the calculated similarity scores as a new column in the DataFrame
    df_restaurant["sim_score"] = sim_scores_list
    
    # Extract the top 10 records with the highest similarity scores
    df_result = df_restaurant.nlargest(10, 'sim_score').copy()

    # Return only the specified columns for the final output
    return df_result[["name", "address", "description"]]