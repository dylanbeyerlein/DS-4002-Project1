from google.cloud import firestore
from google.oauth2 import service_account
import csv


def format_published_date(published_at) -> str:
    if published_at is None:
        return ""
    return published_at.strftime("%B %d, %Y")


PROJECT_ID = "cav-daily"
DB_ID = "cav-daily-articles-puzzles"
KEY_PATH = r"C:\DS4002\Project 1\cav-daily-38a30f321cf4.json"
out_path = r"C:\DS4002\Project 1\news_articles_v2.csv"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
db = firestore.Client(project=PROJECT_ID, database=DB_ID, credentials=credentials)

query = db.collection("articles").where("tags", "array_contains", "news")

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
