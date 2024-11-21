import tweepy

bearer_token = 'AAAAAAAAAAAAAAAAAAAAKhTxAEAAAAADpEKb9pqoNLyqwpkRP8S7%2FJ9B6U%3D57e86Xj60GXAYR94NlIou3gXvfSj3hPaUtk5LTcsA6NOMWFcmj'
client = tweepy.Client(bearer_token)

# Test a simple query
try:
    tweets = client.search_recent_tweets(query="technology", max_results=5)
    for tweet in tweets.data:
        print(tweet.text)
except tweepy.errors.Unauthorized:
    print("Unauthorized: Please check your Bearer Token.")
except Exception as e:
    print(f"Error: {e}")
