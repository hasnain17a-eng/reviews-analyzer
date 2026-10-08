# Customer Review Insights

A Python tool that reads customer reviews from a CSV file, scores each review's
sentiment using **TextBlob**, and prints a summary of what customers feel.

> **Note:** This is a recreated version of my coursework project. The original
> files were lost with my old laptop, so I rebuilt it from scratch. `reviews.csv`
> contains sample reviews written for demonstration.

## What it does
- Reads reviews from `reviews.csv` (columns: `review_id`, `review_text`)
- Calculates **polarity** (-1 negative to +1 positive) and **subjectivity** (0 to 1) for each review
- Labels each review as **Positive**, **Neutral** or **Negative**
- Prints counts, percentages, average polarity, the most positive and most negative review, and common words in positive/negative reviews
- Saves all scores to `results.csv`

## How to run
```bash
pip install -r requirements.txt
python analyze_reviews.py
```
To use your own data, create a CSV with the same two columns and run:
```bash
python analyze_reviews.py my_reviews.csv
```

## How the labels work
| Polarity | Label |
|---|---|
| above 0.1 | Positive |
| -0.1 to 0.1 | Neutral |
| below -0.1 | Negative |

## Tech
Python 3.9+, TextBlob, csv, collections

## Ideas to extend
- Add a chart of sentiment counts with matplotlib
- Analyse reviews by product or date
- Compare TextBlob with another sentiment tool
