

# For data manipulation
import pandas as pd

# Import SentimentIntensityAnalyzer class
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# For plotting data
import matplotlib.pyplot as plt

# Load the news data from a pickle file
# new1 = pd.read_pickle("/Users/algotrading2024/batch 28/20_sentiment_machine_learning/AAPL_news_2016Jan_2023Sep.bz2")
news=pd.read_csv('/Users/algotrading2024/batch 29/news2.csv')
# Print the data
print(news)
# print(new1)
# Extract the date from the 'updated_at' column
news['date'] = [str(x)[:10] for x in news['updated_at']]

print(news)
# # Print the data

# Create an object of SentimentIntensityAnalyzer class
analyzer = SentimentIntensityAnalyzer()

# Calculate the compound sentiment score for each headline
news["compound_score"] = news.headline.apply(
    lambda t: analyzer.polarity_scores(t)['compound'])

# Print the data
print(news)

# Filter out news with non-zero sentiment scores
news_filtered = news.loc[news["compound_score"] != 0, :]

# print(news_filtered)

# Group news by date and count the number of news articles for each date
news_daily_count = news_filtered.groupby(
    "date")["date"].agg('count').to_frame('total_news_articles')

# Print the data
news_daily_count.head()
# Print the data
print(news_daily_count)

# Set the date as the index for the news_filtered dataframe
news_filtered.set_index("date", inplace=True)

# Join the total news count with the news_filtered dataframe
news_filtered = news_filtered.join(news_daily_count, how='outer')

# Print the data
print(news_filtered)

# Calculate the sentiment score by dividing the compound score by the total news articles for each date
news_filtered["sentiment_score"] = news_filtered["compound_score"] / news_filtered["total_news_articles"]

# # Print the data
print(news_filtered)

# Sum the sentiment scores for each date
sum_of_sentiments = news_filtered.sentiment_score.groupby("date").sum()

# Print the data
print(sum_of_sentiments)

# Create the dataframe `daily_sentiment_data`
daily_sentiment_data = pd.DataFrame()

# Calculate the mean total news articles for each date
daily_sentiment_data = news_filtered.groupby("date")[["total_news_articles"]].mean()

# Add the sum of sentiment scores to the daily_sentiment_data dataframe
daily_sentiment_data["sentiment_score"] = sum_of_sentiments

# Print the data
print(daily_sentiment_data)


# # daily_sentiment_data.to_csv('daily_sentiment_scores_2016_jan_2023_sep.csv')