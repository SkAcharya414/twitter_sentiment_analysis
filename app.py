import tweepy
import time
from textblob import TextBlob

# Twitter API credentials (ensure to get the correct bearer token)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFlrxAEAAAAA8zgsuACUDCmD1x4I4nDqigKJTjo%3DEc5WMPShLCEv8oXDVLUynFETu3o0pUgkny4y2WeAupSz8zJFlK'

# Set up Twitter API v2 authentication
client = tweepy.Client(bearer_token=bearer_token)

# Function to clean tweet text (remove unwanted characters)
def clean_tweet(tweet):
    return ' '.join([word for word in tweet.split() if not word.startswith('@') and not word.startswith('http')])

# Function to analyze sentiment of the tweet
def get_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Function to fetch tweets and analyze sentiment using Twitter API v2
def get_tweets_sentiment(query, count=10):
    positive, neutral, negative = 0, 0, 0
    try:
        tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=['text'])
        
        print(f"Sentiment analysis for '{query}'\n")
        
        # Analyze each tweet
        for tweet in tweets.data:
            sentiment = get_sentiment(tweet.text)
            print(f"Tweet: {tweet.text}\nSentiment: {sentiment}\n")
            
            # Count sentiment types
            if sentiment == 'positive':
                positive += 1
            elif sentiment == 'neutral':
                neutral += 1
            else:
                negative += 1
        
        # Print overall sentiment statistics
        total_tweets = len(tweets.data)
        print(f"\nOverall Sentiment Analysis:")
        print(f"Positive tweets: {positive} ({(positive / total_tweets) * 100:.2f}%)")
        print(f"Neutral tweets: {neutral} ({(neutral / total_tweets) * 100:.2f}%)")
        print(f"Negative tweets: {negative} ({(negative / total_tweets) * 100:.2f}%)")
    
    except tweepy.errors.TooManyRequests as e:
        print("Rate limit exceeded. Sleeping for 15 minutes...")
        time.sleep(15 * 60)  # Wait for 15 minutes
        return get_tweets_sentiment(query, count)  # Retry the request after sleeping

# Main function to run the bot
def main():
    query = input("Enter the topic to analyze sentiment: ")
    count = int(input("Enter the number of tweets to analyze (e.g., 10): "))
    
    get_tweets_sentiment(query, count)

if __name__ == "__main__":
    main()
