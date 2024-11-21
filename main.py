from flask import Flask, render_template, request, jsonify
import tweepy
from textblob import TextBlob

# Your Bearer Token (ensure it's correct and not expired)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAKhTxAEAAAAADpEKb9pqoNLyqwpkRP8S7%2FJ9B6U%3D57e86Xj60GXAYR94NlIou3gXvfSj3hPaUtk5LTcsA6NOMWFcmj'

# Set up tweepy client using Bearer Token for authentication
client = tweepy.Client(bearer_token)

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    search_tweet = request.form.get("search_query")
    
    # List to store tweet data
    t = []
    
    try:
        # Fetch tweets using the Twitter API (search tweets using query)
        tweets = client.search_recent_tweets(query=search_tweet, max_results=100, tweet_fields=['text'])
        
        # Process each tweet and analyze sentiment
        for tweet in tweets.data:
            polarity = TextBlob(tweet.text).sentiment.polarity
            subjectivity = TextBlob(tweet.text).sentiment.subjectivity
            t.append([tweet.text, polarity, subjectivity])
        
        # Return the analyzed tweets as JSON response
        return jsonify({"success": True, "tweets": t})

    except tweepy.errors.Unauthorized as e:
        # Handle Unauthorized error (401)
        return jsonify({"success": False, "error": "Unauthorized access. Please check your Bearer Token."})
    
    except Exception as e:
        # Handle other exceptions
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
