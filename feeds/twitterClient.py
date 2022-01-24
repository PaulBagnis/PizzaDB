from tweepy import OAuthHandler, API, Cursor
from tweepy.errors import TweepyException
from polyglot.detect import Detector


class TwitterClient(object):
    def __init__(self, db, sentimentModule, supported_languages=['en']):
        """ 
        DESC : initiate varibles and set-up the tweepy class for later usage

        IN   :  db - database where infos are going to be saved
                sa - sentiment analysis class analyse our string
                supported_language - only fetch certain languages (used for emoji conversion) (default is english) 
        """
        self.db = db
        self.sa = sentimentModule
        self.supported_languages = supported_languages

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

    def insertDb(self, tweets):
        """ 
        DESC : format tweet infos before sending them to the db

        IN   : array of dict containing every infos about their tweet 
        OUT  : array of sorted provided dict 
        """
        actions = []
        for tweet in tweets:
            actions.append({
                '_index': 'twitter',
                '_id': tweet.id_str,
                '_source': {
                    'date': tweet.created_at,
                    'text': tweet.full_text,
                    'polarity': self.sa.calculatePolarity_baseFive(tweet.full_text),
                    'nombre_retweet': tweet.retweet_count,
                    'nombre_like': tweet.favorite_count,
                },
            })
        self.db.insertData(actions)

    def deleteDb(self):
        """ 
        DESC : ask the ElasticSearch db to delete every entries that came from twitter 
        """
        return self.db.deleteData('twitter')

    def getTweets(self, query, count=10):
        """ 
        DESC : download every tweets that match our query then keep only the ones that have the supported languages 

        IN   :  query - search input to fetch tweets
                count - number of tweet to download ( default is 10 )
        OUT  : array of dictionnary containing tweet infos
        """
        tweets = []
        try:
            for tweet in Cursor(self.api.search_tweets, q=query, 
                            tweet_mode='extended').items(count):
                language=Detector(tweet.full_text, quiet=True).language.code
                if language in self.supported_languages:
                    if tweet.retweet_count:
                        if tweet not in tweets:
                            tweets.append(tweet)
                    else:
                        tweets.append(tweet)
            return tweets
        except TweepyException as e:
            print('Error : ' + str(e))

    def pushNewTweets(self, query, count):
        """ 
        DESC : fetch tweets before sending formeted version of them to the DB

        IN   :  query - search input to fetch tweets
                count - number of tweet to download ( default is 10 )
        OUT  : result of the request
        """
        return self.insertDb(self.getTweets(query, count))

    def setSupportedLanguages(self, language):
        """ 
        DESC : basicd setter method

        IN   :  language - new supported language
        """
        self.supported_languages = language
