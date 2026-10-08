"""
Customer Review Insights
Reads customer reviews from a CSV file, scores the sentiment of each review
with TextBlob, and prints a short summary of what customers feel.

Usage:
    python analyze_reviews.py                 # uses reviews.csv
    python analyze_reviews.py my_reviews.csv  # uses your own file
"""
import csv
import sys
from collections import Counter

from textblob import TextBlob

# Reviews with polarity between these values are treated as neutral.
NEUTRAL_LOW = -0.1
NEUTRAL_HIGH = 0.1

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "it", "this",
    "that", "i", "my", "me", "we", "you", "to", "of", "in", "on", "for", "with",
    "very", "so", "as", "at", "be", "have", "has", "had", "not", "no", "they",
    "them", "its", "from", "just", "than", "too", "would", "will", "after", "got",
}


def label_for(polarity: float) -> str:
    if polarity > NEUTRAL_HIGH:
        return "Positive"
    if polarity < NEUTRAL_LOW:
        return "Negative"
    return "Neutral"


def load_reviews(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyze(reviews: list[dict]) -> list[dict]:
    results = []
    for row in reviews:
        text = row["review_text"].strip()
        sentiment = TextBlob(text).sentiment
        results.append({
            "review_id": row["review_id"],
            "review_text": text,
            "polarity": round(sentiment.polarity, 3),
            "subjectivity": round(sentiment.subjectivity, 3),
            "label": label_for(sentiment.polarity),
        })
    return results


def top_words(results: list[dict], label: str, n: int = 5) -> list[tuple[str, int]]:
    counter = Counter()
    for r in results:
        if r["label"] != label:
            continue
        for word in r["review_text"].lower().split():
            word = word.strip(".,!?;:\"'()")
            if len(word) > 2 and word not in STOPWORDS:
                counter[word] += 1
    return counter.most_common(n)


def save_results(results: list[dict], path: str = "results.csv") -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


def print_summary(results: list[dict]) -> None:
    total = len(results)
    counts = Counter(r["label"] for r in results)
    average = sum(r["polarity"] for r in results) / total

    print(f"\nReviews analysed: {total}")
    print("-" * 40)
    for label in ("Positive", "Neutral", "Negative"):
        pct = counts[label] / total * 100
        print(f"{label:<9}: {counts[label]:>3}  ({pct:.0f}%)")
    print(f"\nAverage polarity: {average:+.2f}  (-1 = very negative, +1 = very positive)")

    best = max(results, key=lambda r: r["polarity"])
    worst = min(results, key=lambda r: r["polarity"])
    print(f"\nMost positive review (#{best['review_id']}): {best['review_text']}")
    print(f"Most negative review (#{worst['review_id']}): {worst['review_text']}")

    print("\nCommon words in positive reviews:", top_words(results, "Positive"))
    print("Common words in negative reviews:", top_words(results, "Negative"))


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "reviews.csv"
    reviews = load_reviews(path)
    if not reviews:
        print("No reviews found in the file.")
        return
    results = analyze(reviews)
    save_results(results)
    print_summary(results)
    print("\nFull results saved to results.csv")


if __name__ == "__main__":
    main()
