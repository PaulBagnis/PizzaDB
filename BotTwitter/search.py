from ast import Param
from operator import index
import tweepy
from datetime import datetime
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
from elasticsearch import Elasticsearch , helpers

auth = tweepy.OAuthHandler('n4QQQaLtC70dsi54adwRuFMCW', 'GrsLdf2drgLFkT8FpFzPeLrBrFTFlHY4LN6h7EiVamY7GefiHE')
auth.set_access_token('1377622154683019265-wB6k2RuIfNGcth52wDEO6bGPnzyXYw', '8RTqizUFIrmg7LAAawJXDwZF7w1qHoPdypvpIRYd6ji5B')
api = tweepy.API(auth)
es = Elasticsearch()
tab=[]
bulk_n= 150
tweets = tweepy.Cursor(api.search_tweets,
              lang="fr", q="one_piece"+ " -filter:retweets").items(bulk_n)
for tweet in tweets:
    tab.append({'id': tweet.id_str, 'date': tweet.created_at, 'texte': tweet.text, 'nombre_retweet': tweet.retweet_count, 'nombre_like' : tweet.favorite_count})    


tw= helpers.bulk(es, tab, index= "hashtag")