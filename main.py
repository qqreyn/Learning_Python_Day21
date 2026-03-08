"""
News Automation Tool
====================
Fetches top headlines, cleans & analyzes the data,
generates a report, and saves everything to disk.

API used: NewsAPI (https://newsapi.org) — free tier available.
Get your free API key at: https://newsapi.org/register
"""

import os
import json
import csv
import logging
import requests
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION  ← change these to experiment!
# ─────────────────────────────────────────────
API_KEY   = "YOUR_API_KEY_HERE"   # paste your NewsAPI key here
TOPIC     = "technology"          # try: sports, science, business, health
MAX_ARTICLES = 10                 # how many articles to fetch

# File paths
RAW_DATA_FILE    = "raw_data.json"
HISTORY_FILE     = "history.csv"
REPORT_FILE      = "report.txt"
LOG_FILE         = "automation.log"


# ─────────────────────────────────────────────
# STEP 0 — SET UP LOGGING
# ─────────────────────────────────────────────
# Logging records what your program is doing at each step.
# It writes to BOTH your console AND a .log file at once.
logging.basicConfig(
    level=logging.INFO,                          # INFO = normal messages
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),           # save to file
        logging.StreamHandler()                  # also print to console
    ]
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# STEP 1 — FETCH DATA FROM API
# ─────────────────────────────────────────────
def fetch_news(topic, api_key, max_results=10):
    """
    Calls the NewsAPI and returns raw JSON data.
    
    🧪 Experiment:
      - Change topic to "sports" or "science"
      - Change max_results to 5 or 20
      - Print the raw `response_data` to see the full API response
    """
    logger.info(f"Fetching news for topic: '{topic}'")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q":        topic,
        "apiKey":   api_key,
        "pageSize": max_results,
        "language": "en",
        "sortBy":   "publishedAt"   # newest first
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()          # raises error if status != 200
        response_data = response.json()

        if response_data.get("status") != "ok":
            raise ValueError(f"API error: {response_data.get('message')}")

        articles = response_data.get("articles", [])
        logger.info(f"Successfully fetched {len(articles)} articles")
        return articles

    except requests.exceptions.ConnectionError:
        logger.error("No internet connection. Could not reach the API.")
        raise
    except requests.exceptions.Timeout:
        logger.error("Request timed out. The API took too long to respond.")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        raise


# ─────────────────────────────────────────────
# STEP 2 — CLEAN & PROCESS DATA
# ─────────────────────────────────────────────
def clean_articles(raw_articles):
    """
    Takes the messy raw API data and keeps only what we need.
    Also handles missing fields so the program doesn't crash.

    🧪 Experiment:
      - Add "url" to the kept fields below
      - Print one raw article vs one cleaned article — spot the difference
      - Try removing the `or "Unknown"` fallbacks and see what breaks
    """
    logger.info("Cleaning and processing articles...")
    cleaned = []

    for article in raw_articles:
        # Skip articles with no title or content
        if not article.get("title") or article["title"] == "[Removed]":
            logger.warning("Skipped an article with no title.")
            continue

        cleaned.append({
            "title":       article.get("title",       "Unknown Title"),
            "source":      article.get("source", {}).get("name", "Unknown Source"),
            "author":      article.get("author",      "Unknown Author"),
            "published_at": article.get("publishedAt", "Unknown Date"),
            "description": article.get("description", "No description available.")
        })

    logger.info(f"{len(cleaned)} articles after cleaning")
    return cleaned


# ─────────────────────────────────────────────
# STEP 3 — ANALYZE DATA
# ─────────────────────────────────────────────
def analyze_articles(articles):
    """
    Counts and summarizes the cleaned data.

    🧪 Experiment:
      - Add a count of articles published today vs older
      - Find the most common word in all titles (hint: use .split())
      - Add average title length: sum(len(a["title"]) for a in articles) / len(articles)
    """
    logger.info("Analyzing articles...")

    if not articles:
        return {}

    # Count articles per source
    source_counts = {}
    for article in articles:
        source = article["source"]
        source_counts[source] = source_counts.get(source, 0) + 1

    # Sort sources by article count (most first)
    sorted_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)

    analysis = {
        "total_articles":   len(articles),
        "unique_sources":   len(source_counts),
        "top_source":       sorted_sources[0][0] if sorted_sources else "N/A",
        "source_breakdown": dict(sorted_sources),
        "fetched_at":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logger.info(f"Analysis complete. Top source: {analysis['top_source']}")
    return analysis


# ─────────────────────────────────────────────
# STEP 4 — GENERATE REPORT
# ─────────────────────────────────────────────
def generate_report(articles, analysis, topic):
    """
    Builds a nicely formatted text report and:
      1. Prints it to the console
      2. Saves it to report.txt

    🧪 Experiment:
      - Add a section that lists all article URLs
      - Change the banner style (the === lines)
      - Add a "Most Recent Article" section using articles[0]
    """
    logger.info("Generating report...")

    now    = analysis.get("fetched_at", "N/A")
    border = "=" * 60

    lines = [
        border,
        f"  NEWS AUTOMATION REPORT",
        f"  Topic    : {topic.upper()}",
        f"  Generated: {now}",
        border,
        "",
        "SUMMARY",
        "-" * 30,
        f"  Total articles   : {analysis.get('total_articles', 0)}",
        f"  Unique sources   : {analysis.get('unique_sources', 0)}",
        f"  Top source       : {analysis.get('top_source', 'N/A')}",
        "",
        "SOURCE BREAKDOWN",
        "-" * 30,
    ]

    for source, count in analysis.get("source_breakdown", {}).items():
        bar = "█" * count                        # visual bar chart!
        lines.append(f"  {source:<30} {bar} ({count})")

    lines += [
        "",
        "TOP HEADLINES",
        "-" * 30,
    ]

    for i, article in enumerate(articles[:5], start=1):   # top 5 only
        lines.append(f"\n  [{i}] {article['title']}")
        lines.append(f"      Source : {article['source']}")
        lines.append(f"      Author : {article['author']}")
        lines.append(f"      Date   : {article['published_at']}")
        lines.append(f"      Desc   : {article['description'][:80]}...")

    lines += ["", border, "  END OF REPORT", border]

    report_text = "\n".join(lines)

    # Print to console
    print(report_text)

    # Save to file
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

    logger.info(f"Report saved to '{REPORT_FILE}'")
    return report_text


# ─────────────────────────────────────────────
# STEP 5 — SAVE RAW DATA & HISTORY
# ─────────────────────────────────────────────
def save_raw_data(raw_articles, topic):
    """
    Saves full raw API response to a JSON file for record-keeping.

    🧪 Experiment:
      - Run the script twice and open raw_data.json — does it update?
      - Change the filename to include the date: f"raw_{topic}_{today}.json"
    """
    payload = {
        "topic":      topic,
        "fetched_at": datetime.now().isoformat(),
        "articles":   raw_articles
    }
    with open(RAW_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    logger.info(f"Raw data saved to '{RAW_DATA_FILE}'")


def append_to_history(analysis, topic):
    """
    Adds one summary row to history.csv every time the script runs.
    Over time this builds a historical record you can open in Excel.

    🧪 Experiment:
      - Run the script 3 times — open history.csv and see all rows
      - Add a "topic" column to track different topics over time
    """
    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["fetched_at", "topic", "total_articles", "unique_sources", "top_source"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()                 # only write header on first run

        writer.writerow({
            "fetched_at":     analysis.get("fetched_at"),
            "topic":          topic,
            "total_articles": analysis.get("total_articles"),
            "unique_sources": analysis.get("unique_sources"),
            "top_source":     analysis.get("top_source")
        })

    logger.info(f"History updated in '{HISTORY_FILE}'")


# ─────────────────────────────────────────────
# MAIN — WIRES EVERYTHING TOGETHER
# ─────────────────────────────────────────────
def main():
    logger.info("─── Automation tool started ───")

    try:
        # 1. Fetch
        raw_articles = fetch_news(TOPIC, API_KEY, MAX_ARTICLES)

        # 2. Clean
        clean = clean_articles(raw_articles)

        # 3. Analyze
        analysis = analyze_articles(clean)

        # 4. Report
        generate_report(clean, analysis, TOPIC)

        # 5. Save
        save_raw_data(raw_articles, TOPIC)
        append_to_history(analysis, TOPIC)

        logger.info("─── All steps completed successfully ───")

    except Exception as e:
        logger.error(f"Script failed: {e}")
        print(f"\n❌ Something went wrong: {e}")
        print("Check automation.log for details.")


# Only runs main() if you execute THIS file directly
# (won't run if another file imports this one)
if __name__ == "__main__":
    main()
