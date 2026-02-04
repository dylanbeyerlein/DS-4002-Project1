"""
DS 4002 Project 1
Script Name: export_articles.py
Description:
    This script connects to a Google Firestore database containing
    Cavalier Daily article data. It authenticates using a service
    account key, queries for all articles tagged as "news", extracts
    selected fields (document ID, authors, publication date, section,
    and title), formats the data, and writes it to a CSV file.

    This script is part of the data collection pipeline for analyzing
    word frequencies in Cavalier Daily article titles.
"""
# Import required libraries

from google.cloud import firestore
from google.oauth2 import service_account
import csv

# Helper function to format dates
def format_published_date(published_at) -> str:
    """
    Converts a Firestore timestamp into a human-readable date string.
    If the timestamp is missing, returns an empty string.
    """
    if published_at is None:
        return ""
    return published_at.strftime("%B %d, %Y")

# Configuration variables
PROJECT_ID = "cav-daily"  
DB_ID = "cav-daily-articles-puzzles" 
KEY_PATH = r"C:\DS4002\Project 1\cav-daily-38a30f321cf4.json"  
out_path = r"C:\DS4002\Project 1\news_articles_v2.csv"

# Authenticate and connect to Firestore
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

# Create a Firestore client using the project, database, and credentials
db = firestore.Client(
    project=PROJECT_ID,
    database=DB_ID,
    credentials=credentials
)

# Define Firestore query
# Query the "articles" collection for documents where the "tags" array contains "news"
query = db.collection("articles").where("tags", "array_contains", "news")

# Write query results to CSV
with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["doc_id", "authors", "published_date", "section", "title"])

    count = 0  
    for doc in query.stream():
        data = doc.to_dict() 
        doc_id = doc.id
        authors = data.get("authors", [])
        if not isinstance(authors, list):
            authors = [str(authors)]

        published_at = data.get("published_at")
        published_date = format_published_date(published_at)

        section = "News"

        title = data.get("title", "")

        writer.writerow([
            doc_id,
            "; ".join(authors), 
            published_date,
            section,
            title
        ])

        count += 1 
print(f"Wrote {count} rows to {out_path}")
