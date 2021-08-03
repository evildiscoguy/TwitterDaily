import tweepy
import requests
import random

from credentials import keys

API_KEY = keys["API_KEY"]
API_SECRET_KEY = keys["API_SECRET_KEY"]
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

file = open("last_tweet.txt", "r")
last_tweet = int(file.readline())
file.close()

quotes = requests.get("https://type.fit/api/quotes")

mentions = api.mentions_timeline(last_tweet, tweet_mode="extended")

for mention in reversed(mentions):
    last_tweet = mention.id

    if "#edgquote" in mention.full_text.lower():
        try:
            random_quote = random.choice(quotes.json())
            quote_to_tweet = random_quote['text'] + " - " + random_quote['author']
            # print(mention.full_text)
            message = quote_to_tweet + " #edgquote"
            api.create_favorite(mention.id)
            api.update_status(message, mention.id)
            # print(message)
        except tweepy.error.TweepError as e:
            print(e)

file = open("last_tweet.txt", "w")
file.write(str(last_tweet))
file.close()
