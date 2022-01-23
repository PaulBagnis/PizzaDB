from tweepy import OAuthHandler, API, Cursor
from tweepy.errors import TweepyException


class TwitterClient(object):
    def __init__(self, db, sentimentModule):
        self.db = db
        self.sa = sentimentModule

        consumer_key = "n4QQQaLtC70dsi54adwRuFMCW"
        consumer_secret = "GrsLdf2drgLFkT8FpFzPeLrBrFTFlHY4LN6h7EiVamY7GefiHE"
        access_token = "1377622154683019265-wB6k2RuIfNGcth52wDEO6bGPnzyXYw"
        access_token_secret = "8RTqizUFIrmg7LAAawJXDwZF7w1qHoPdypvpIRYd6ji5B"

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = API(self.auth)
        except:
            print("Error: Authentication Failed")

    def insertDb(self, tweets):
        actions = []
        for tweet in tweets:
            actions.append({
                '_index': 'twitter',
                '_id': tweet.id_str,
                '_source': {
                    'data': tweet.created_at,
                    'text': tweet.text,
                    'polarity': self.sa.calculatePolarity_baseFive(tweet.text),
                    'nombre_retweet': tweet.retweet_count,
                    'nombre_like': tweet.favorite_count
                }
            })
        self.db.insertData(actions)
        
    def deleteDb(self):
        return self.db.deleteData('twitter')

    def getTweets(self, query, count=10):
        tweets = []
        try:
            for tweet in Cursor(self.api.search_tweets, q=query).items(count):
                if tweet.retweet_count:
                    if tweet not in tweets:
                        tweets.append(tweet)
                else:
                    tweets.append(tweet)
            return tweets
        except TweepyException as e:
            print("Error : " + str(e))

    def pushNewTweets(self, query, count):
        return self.insertDb(self.getTweets(query, count))
