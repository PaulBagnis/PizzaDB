#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv
from datetime import datetime
from elasticsearch import Elasticsearch , helpers
#http://www.tweepy.org/
import tweepy
es = Elasticsearch()
#Get your Twitter API credentials and enter them here
consumer_key = "n4QQQaLtC70dsi54adwRuFMCW"
consumer_secret = "GrsLdf2drgLFkT8FpFzPeLrBrFTFlHY4LN6h7EiVamY7GefiHE"
access_key = "1377622154683019265-wB6k2RuIfNGcth52wDEO6bGPnzyXYw"
access_secret = "8RTqizUFIrmg7LAAawJXDwZF7w1qHoPdypvpIRYd6ji5B"


#http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

	#set count to however many tweets you want
number_of_tweets = 100
tweets = tweepy.Cursor(api.user_timeline, screen_name = "jtakoutsing")

	#get tweets
tweets_for_csv = []
for tweet in tweets.items(number_of_tweets):
        #create array of tweet information: jtakoutsing, tweet id, date/time, text
		tweets_for_csv.append({'id': tweet.id_str, 'date': tweet.created_at, 'texte': tweet.text})

helpers.bulk(es, tweets_for_csv, index= "account")