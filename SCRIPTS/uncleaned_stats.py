"""
DS 4002 Project 1
Script Name: uncleaned_stats.py
Description:
    This script computes summary statistics and generates plots for the
    uncleaned News/Opinion article dataset. It reads an uncleaned CSV,
    computes title word counts and parsed publication dates, computes
    headline dataset metrics (article count, unique authors, title length
    statistics, and date range), writes a one-row summary CSV, and saves
    figures (title-length histogram and articles-by-month line plot) to
    the OUTPUTS directory.
"""


# Import required libraries
import os
import re
import pandas as pd
import matplotlib.pyplot as plt


# Change to "opinion"
DATASET = "news"


# Count the number of words in a title
def title_word_count(title: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9]+(?:['\u2019.\-][A-Za-z0-9]+)*", str(title).strip())
    return len(tokens)


# Split an authors string into a list of author names
def split_authors(authors: str) -> list[str]:
    return [a.strip() for a in str(authors).split(";") if a.strip()]


# Build the input/output file paths
def build_paths(dataset: str) -> tuple[str, str, str]:
    input_csv = "C:/DS4002/Project 1/text_analysis/DATA/raw/" + dataset + "_uncleaned.csv"
    output_csv = "C:/DS4002/Project 1/text_analysis/OUTPUTS/tables/" + dataset + "_uncleaned_summary.csv"
    output_fig_dir = "C:/DS4002/Project 1/text_analysis/OUTPUTS/figures/" + dataset + "_uncleaned"
    return input_csv, output_csv, output_fig_dir


# Ensure the output directories exist before writing results
def ensure_output_locations(output_csv: str, output_fig_dir: str) -> None:
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(output_fig_dir, exist_ok=True)


# Load the cleaned dataset CSV into a DataFrame
def load_articles_csv(input_csv: str) -> pd.DataFrame:
    return pd.read_csv(input_csv, dtype=str, encoding="utf-8-sig")


# Add parsed dates and title word counts as new columns
def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    derived_df = df.copy()
    derived_df["published_dt"] = pd.to_datetime(derived_df["published_date"], format="%d-%b-%y", errors="coerce")
    derived_df["title_word_count"] = derived_df["title"].map(title_word_count)
    return derived_df


# Count the number of unique authors across all articles
def count_unique_authors(df: pd.DataFrame) -> int:
    all_authors = []
    for a in df["authors"]:
        all_authors.extend(split_authors(a))
    return len(set(all_authors))


# Compute the date range covered by the dataset
def compute_date_range(published_dt: pd.Series) -> str:
    start_date = published_dt.min().strftime("%B %Y")
    end_date = published_dt.max().strftime("%B %Y")
    return start_date + " - " + end_date


# Create the one-row summary DataFrame
def create_summary_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    title_counts = df["title_word_count"]
    return pd.DataFrame([{
        "total_articles": len(df),
        "num_unique_authors": count_unique_authors(df),
        "avg_title_len": round(title_counts.mean(), 2),
        "med_title_len": round(title_counts.median(), 2),
        "min_title_len": int(title_counts.min()),
        "max_title_len": int(title_counts.max()),
        "date_range": compute_date_range(df["published_dt"])
    }])


# Write the summary DataFrame to a CSV file
def write_summary_csv(summary_df: pd.DataFrame, output_csv: str) -> None:
    summary_df.to_csv(output_csv, index=False, encoding="utf-8-sig")


# Compute the number of articles published per month
def compute_monthly_article_counts(df: pd.DataFrame) -> pd.DataFrame:
    df_with_month = df.copy()
    df_with_month["year_month"] = df_with_month["published_dt"].dt.to_period("M").astype(str)
    monthly_counts = df_with_month.groupby("year_month").size().reset_index(name="article_count")
    return monthly_counts.sort_values("year_month")


# Plot and save a histogram of title word counts
def plot_title_length_histogram(title_counts: pd.Series, output_fig_dir: str, dataset: str) -> None:
    plt.figure()
    plt.hist(title_counts, bins=30)
    plt.xlabel("Number of words per title")
    plt.ylabel("Frequency")
    plt.title(dataset.capitalize() + "_Uncleaned: Distribution of Title Lengths")
    plt.tight_layout()
    plt.savefig(os.path.join(output_fig_dir, "title_length_hist.png"))
    plt.close()


# Plot and save a line chart of article counts by month
def plot_articles_by_month(monthly_counts: pd.DataFrame, output_fig_dir: str, dataset: str) -> None:
    plt.figure()
    plt.plot(monthly_counts["year_month"], monthly_counts["article_count"], marker="o")
    plt.xlabel("Month")
    plt.ylabel("Number of Articles")
    plt.title(dataset.capitalize() + "_Uncleaned: Number of Articles by Month")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_fig_dir, dataset + "_articles_by_month.png"))
    plt.close()


# Print a short summary to console
def print_run_summary(output_csv: str, output_fig_dir: str, summary_df: pd.DataFrame) -> None:
    row = summary_df.iloc[0].to_dict()
    print("Wrote summary CSV to:", output_csv)
    print("Wrote figures to:", output_fig_dir)
    print("Total articles:", row["total_articles"])
    print("Unique authors:", row["num_unique_authors"])
    print("Date range:", row["date_range"])


# Run the full script (load/summarize/plot/print)
def main() -> None:
    input_csv, output_csv, output_fig_dir = build_paths(DATASET)
    ensure_output_locations(output_csv, output_fig_dir)

    df = load_articles_csv(input_csv)
    df = add_derived_columns(df)

    summary_df = create_summary_dataframe(df)
    write_summary_csv(summary_df, output_csv)

    plot_title_length_histogram(df["title_word_count"], output_fig_dir, DATASET)

    monthly_counts = compute_monthly_article_counts(df)
    plot_articles_by_month(monthly_counts, output_fig_dir, DATASET)

    print_run_summary(output_csv, output_fig_dir, summary_df)


if __name__ == "__main__":
    main()
