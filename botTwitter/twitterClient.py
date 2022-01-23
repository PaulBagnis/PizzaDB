from tweepy import OAuthHandler, API, Cursor
from tweepy.errors import TweepyException

class TwitterClient(object):
    def __init__(self, sentimentModule, db):
        self.sm = sentimentModule
        self.db = db

        consumer_key = 'n4QQQaLtC70dsi54adwRuFMCW'
        consumer_secret = 'GrsLdf2drgLFkT8FpFzPeLrBrFTFlHY4LN6h7EiVamY7GefiHE'
        access_token = '1377622154683019265-wB6k2RuIfNGcth52wDEO6bGPnzyXYw'
        access_token_secret = '8RTqizUFIrmg7LAAawJXDwZF7w1qHoPdypvpIRYd6ji5B'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = API(self.auth)
        except:
            print('Error: Authentication Failed')


    def get_tweets(self, query, count = 10):
        tweets = []
        try:
            for tweet in Cursor(self.api.search_tweets, q=query).items(count):
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.sm.calculatePolarity(tweet.text)
                if tweet.retweet_count:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
            
        except TweepyException as e:
            print('Error : ' + str(e))
