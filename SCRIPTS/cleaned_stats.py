"""
DS 4002 Project 1
Script Name: cleaned_stats.py
Description:
    This script computes summary statistics and generates plots for the
    cleaned News/Opinion title token dataset. It reads a cleaned CSV,
    parses the token lists, computes token/word frequency metrics, writes
    a one-row summary CSV, and saves figures (top words, frequency rank
    plot, token-length histogram) to the OUTPUTS directory.
"""


# Import required libraries
import os
import ast
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


# Change to "opinion"
DATASET = "news"


# Parse a token list stored as a string to a list
def parse_tokens(token_str: str) -> list[str]:
    return ast.literal_eval(token_str)


# Build the input/output file paths
def build_paths(dataset: str) -> tuple[str, str, str]:
    input_csv = "C:/DS4002/Project 1/text_analysis/DATA/cleaned/" + dataset + "_cleaned.csv"
    output_csv = "C:/DS4002/Project 1/text_analysis/OUTPUTS/tables/" + dataset + "_cleaned_summary.csv"
    output_fig_dir = "C:/DS4002/Project 1/text_analysis/OUTPUTS/figures/" + dataset + "_cleaned"
    return input_csv, output_csv, output_fig_dir


# Ensure the output directories exist before writing results
def ensure_output_locations(output_csv: str, output_fig_dir: str) -> None:
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(output_fig_dir, exist_ok=True)


# Load the cleaned dataset CSV into a DataFrame
def load_articles_csv(input_csv: str) -> pd.DataFrame:
    return pd.read_csv(input_csv, dtype=str, encoding="utf-8-sig")


# Parse the token lists from the DataFrame
def get_tokens_per_title(df: pd.DataFrame) -> list[list[str]]:
    return df["tokens"].map(parse_tokens).tolist()


# Combine a list of token lists into one list
def combine_tokens(tokens_per_title: list[list[str]]) -> list[str]:
    all_tokens = []
    for t in tokens_per_title:
        all_tokens.extend(t)
    return all_tokens


# Compute the number of tokens in each title
def compute_token_counts_per_title(tokens_per_title: list[list[str]]) -> list[int]:
    return [len(t) for t in tokens_per_title]


# Compute word frequencies across all titles
def compute_word_counts(all_tokens: list[str]) -> Counter:
    return Counter(all_tokens)


# Compute the percent of words that appear exactly once
def compute_pct_words_appearing_once(word_counts: Counter) -> float:
    num_unique_words = len(word_counts)
    num_words_appearing_once = sum(1 for c in word_counts.values() if c == 1)
    return round((num_words_appearing_once / num_unique_words) * 100, 2)


# Compute the summary statistics for token counts per title (total/avg/median/min/max)
def compute_token_length_stats(token_counts_per_title: list[int]) -> dict:
    s = pd.Series(token_counts_per_title)
    return {
        "total_titles": int(s.size),
        "total_tokens": int(s.sum()),
        "avg_tokens_per_title": round(float(s.mean()), 2),
        "med_tokens_per_title": round(float(s.median()), 2),
        "min_tokens_per_title": int(s.min()),
        "max_tokens_per_title": int(s.max()),
    }


# Create the one-row summary DataFrame
def create_summary_dataframe(tokens_per_title: list[list[str]], dataset: str) -> tuple[pd.DataFrame, Counter, list[int]]:
    token_counts_per_title = compute_token_counts_per_title(tokens_per_title)
    all_tokens = combine_tokens(tokens_per_title)
    word_counts = compute_word_counts(all_tokens)

    token_stats = compute_token_length_stats(token_counts_per_title)
    pct_words_appearing_once = compute_pct_words_appearing_once(word_counts)

    summary_df = pd.DataFrame([{
        "total_" + dataset + "_titles": token_stats["total_titles"],
        "total_tokens": token_stats["total_tokens"],
        "total_unique_words": len(word_counts),
        "avg_tokens_per_title": token_stats["avg_tokens_per_title"],
        "med_tokens_per_title": token_stats["med_tokens_per_title"],
        "min_tokens_per_title": token_stats["min_tokens_per_title"],
        "max_tokens_per_title": token_stats["max_tokens_per_title"],
        "pct_words_appearing_once": pct_words_appearing_once
    }])

    return summary_df, word_counts, token_counts_per_title


# Write the summary DataFrame to a CSV file
def write_summary_csv(summary_df: pd.DataFrame, output_csv: str) -> None:
    summary_df.to_csv(output_csv, index=False, encoding="utf-8-sig")


# Plot and save a bar chart of the top N most frequent words
def plot_top_words(word_counts: Counter, output_fig_dir: str, dataset: str, n: int = 20) -> None:
    top_n = word_counts.most_common(n)
    top_df = pd.DataFrame(top_n, columns=["word", "frequency"])

    plt.figure()
    plt.bar(top_df["word"], top_df["frequency"])
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.title(dataset.capitalize() + "_Cleaned: Top 20 Most Frequent Words")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_fig_dir, dataset + "_top20_words.png"))
    plt.close()


# Plot and save the word frequency distribution
def plot_word_frequency_distribution(word_counts: Counter, output_fig_dir: str, dataset: str) -> None:
    frequencies_sorted = sorted(word_counts.values(), reverse=True)
    ranks = list(range(1, len(frequencies_sorted) + 1))

    plt.figure()
    plt.plot(ranks, frequencies_sorted)
    plt.xlabel("Word rank")
    plt.ylabel("Frequency")
    plt.title(dataset.capitalize() + "_Cleaned: Word Frequency Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_fig_dir, dataset + "_word_frequency_distribution.png"))
    plt.close()


# Plot and save a histogram of token counts per title
def plot_token_length_distribution(token_counts_per_title: list[int], output_fig_dir: str, dataset: str) -> None:
    plt.figure()
    plt.hist(token_counts_per_title, bins=30)
    plt.xlabel("Number of tokens per title")
    plt.ylabel("Frequency")
    plt.title(dataset.capitalize() + "_Cleaned: Token Length Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_fig_dir, dataset + "_token_length_distribution.png"))
    plt.close()


# Print a short summary to console
def print_run_summary(output_csv: str, output_fig_dir: str, summary_df: pd.DataFrame, dataset: str) -> None:
    row = summary_df.iloc[0].to_dict()
    print("Wrote summary CSV to:", output_csv)
    print("Wrote figures to:", output_fig_dir)
    print("Total titles:", row["total_" + dataset + "_titles"])
    print("Total tokens:", row["total_tokens"])
    print("Unique words:", row["total_unique_words"])
    print("% words appearing once:", row["pct_words_appearing_once"])


# Run the full script (load/summarize/plot/print)
def main() -> None:
    input_csv, output_csv, output_fig_dir = build_paths(DATASET)
    ensure_output_locations(output_csv, output_fig_dir)

    df = load_articles_csv(input_csv)
    tokens_per_title = get_tokens_per_title(df)

    summary_df, word_counts, token_counts_per_title = create_summary_dataframe(tokens_per_title, DATASET)
    write_summary_csv(summary_df, output_csv)

    plot_top_words(word_counts, output_fig_dir, DATASET, n=20)
    plot_word_frequency_distribution(word_counts, output_fig_dir, DATASET)
    plot_token_length_distribution(token_counts_per_title, output_fig_dir, DATASET)

    print_run_summary(output_csv, output_fig_dir, summary_df, DATASET)


if __name__ == "__main__":
    main()
