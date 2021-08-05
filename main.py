import tweepy
import requests
import random

from credentials import keys

# Load the data from credentials.py
API_KEY = keys["API_KEY"]
API_SECRET_KEY = keys["API_SECRET_KEY"]
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

# Set tweepy up for use
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Open last_tweet.txt and create a new variable from the data
try:
    with open("last_tweet.txt", "r") as save_id:
        last_tweet = int(save_id.readline())
except FileNotFoundError:
    with open("last_tweet.txt", "w") as save_id:
        save_id.write("1")
        last_tweet = 1

# Create variable with link to quote database
quotes = requests.get("https://type.fit/api/quotes")

# Get most recent @mentions, ignoring those before the last @mention in last_tweet
mentions = api.mentions_timeline(last_tweet, tweet_mode="extended")

# Loop through each @mention backwards as the newest is stored as the first
for mention in reversed(mentions):
    # Update last_tweet with details of the @mention
    last_tweet = mention.id

    # Change "#edgquote" to fit your own usage needs
    # Search for term in mentions
    if "#edgquote" in mention.full_text.lower():
        try:
            # Save user who @mentioned you
            reply_to = mention.user.screen_name

            # Choose a random quote
            random_quote = random.choice(quotes.json())

            # Compose tweet for reply
            quote_to_tweet = random_quote['text'] + " - " + random_quote['author']

            # Change "#edgquote" to fit your own usage needs
            # Set message to send to @mention
            message = "@" + reply_to + " " + quote_to_tweet + " #edgquote"

            # Favourite the @mention
            api.create_favorite(mention.id)

            # Send reply to @mention with quote
            api.update_status(message, mention.id)
        except tweepy.error.TweepError as e:
            # Print error message for debug
            print(e)

# Once finished, write the last_tweet variable to text file
try:
    with open("last_tweet.txt", "w") as save_id:
        save_id.write(str(last_tweet))
except FileNotFoundError:
    with open("last_tweet.txt", "w") as save_id:
        save_id.write("1")
        last_tweet = int(save_id.readline())
