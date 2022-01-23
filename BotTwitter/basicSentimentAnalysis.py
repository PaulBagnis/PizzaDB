import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	def __init__(self):
		consumer_key = 'n4QQQaLtC70dsi54adwRuFMCW'
		consumer_secret = 'GrsLdf2drgLFkT8FpFzPeLrBrFTFlHY4LN6h7EiVamY7GefiHE'
		access_token = '1377622154683019265-wB6k2RuIfNGcth52wDEO6bGPnzyXYw'
		access_token_secret = '8RTqizUFIrmg7LAAawJXDwZF7w1qHoPdypvpIRYd6ji5B'
		try:
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))
		if analysis.sentiment.polarity > 0:
			return 'pos'
		elif analysis.sentiment.polarity == 0:
			return 'neu'
		else:
			return 'neg'

	def get_tweets(self, query, count = 10):
		tweets = []
		try:
			for tweet in tweepy.Cursor(self.api.search_tweets, q=query).items(count):
				parsed_tweet = {}
				parsed_tweet['text'] = tweet.text
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				if tweet.retweet_count:
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			return tweets

		except tweepy.errors.TweepyException as e:
			print("Error : " + str(e))

def percentage(part,whole):
    return format(100 * float(part)/float(whole), '.1f')

def main():
	api = TwitterClient()
	tweets = api.get_tweets(query = 'titanfall2', count = 300)
	pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'pos']
	print("Positive tweets percentage: {} %".format( percentage(len(pos_tweets), len(tweets)) ))
	neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neg']
	print("Negative tweets percentage: {} %".format( percentage(len(neg_tweets), len(tweets)) ))
	neu_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neu']
	print("Neutral tweets percentage: {} %".format( percentage(len(neu_tweets),  len(tweets)) ))

if __name__ == "__main__":
	main()
