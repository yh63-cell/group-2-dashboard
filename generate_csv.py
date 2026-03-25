import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

print("Loading data...")
df = pd.read_csv("src/data/sony_cleaned_data.csv")
vader = SentimentIntensityAnalyzer()

def get_vader_sentiment(text):
    try:
        scores = vader.polarity_scores(str(text))
        return scores['compound']
    except:
        return 0

def classify_sentiment(score):
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

print("Running VADER sentiment analysis. This might take a few seconds...")
df['vader_score'] = df['clean_text'].apply(get_vader_sentiment)
df['sentiment_category'] = df['vader_score'].apply(classify_sentiment)

output_path = "src/data/sony_sentiment_scored.csv"
df.to_csv(output_path, index=False)
print(f"Success! Saved to {output_path}")
