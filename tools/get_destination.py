# tools/get_destination.py

import pandas as pd
import difflib
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database connection URL and initialize the SQLAlchemy engine
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def get_destination(filter_tags: str) -> pd.DataFrame:
    """
    Fetches destination data from the database and returns the top 5 matches
    based on the similarity between the user's filter tags and the destination's category.
    """
    
    # Define the SQL query to fetch necessary columns from the 'destination' table
    query = text("SELECT name, category, address, description, gps_lat, gps_lon FROM destination")
    
    # Execute the query and load the result into a Pandas DataFrame
    df_destination = pd.read_sql(query, engine)

    # Handle the case where the database returns an empty result
    if df_destination.empty:
        return pd.DataFrame(columns=["name", "address", "description", "gps_lat", "gps_lon"])

    # Normalize the input filter tags to lowercase for accurate comparison
    filter_tags_lower = str(filter_tags).lower()
    sim_scores_list = []

    # Iterate through each category in the DataFrame to calculate similarity
    for tag in df_destination["category"]:
        # Normalize the database category tag to lowercase
        tag_lower = str(tag).lower()

        # Calculate the string similarity score (returns a float between 0.0 and 1.0)
        score = difflib.SequenceMatcher(None, filter_tags_lower, tag_lower).ratio()

        # Convert the float score to a percentage format with 2 decimals (e.g., 90.50)
        score_percentage = round(score * 100, 2)
        sim_scores_list.append(score_percentage)

    # Append the calculated similarity scores as a new column in the DataFrame
    df_destination["sim_score"] = sim_scores_list

    # Extract the top 5 records with the highest similarity scores
    df_result = df_destination.nlargest(10, 'sim_score').copy()

    # Return only the specified columns for the final output
    return df_result[["name", "address", "description", "gps_lat", "gps_lon"]]