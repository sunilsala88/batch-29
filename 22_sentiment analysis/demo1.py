

sentence='amzn stock'




# Import SentimentIntensityAnalyzer class
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create an object of SentimentIntensityAnalyzer class
analyzer = SentimentIntensityAnalyzer()

a=analyzer.polarity_scores(sentence)

# Print the data
print(a)