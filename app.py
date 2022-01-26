#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__authors__ = ("Guern Francois", "Bagnis Paul", "Takoutsink Jerry")
__email__ = ("francois.guern@ynov.com", "paul.bagnis@ynov.com", "jerry.takoutsing@ynov.com")
__copyright__ = "MIT"
__date__ = "2022-01-28"
__version__= "0.1.0"
__status__ = "Development"

"""
This project was developed to practice notions view in class mainly about database paradigms.
The contrains were to use different sources of data, in at least two different languages. 
We also had to use different databases with their own paradigms. 
Lastly we had to set up HDFS in any ways.

We decided to focuse on movies on this project, the reasons : a lot of free data online.
We choose to use 3 differents feeds:
TMDB -> The movie DataBase provide an API to fetch any data they had (https://www.themoviedb.org/).
Twitter -> The social media give access to every messages posted on their website (https://twitter.com/).
NewRSS -> Every now and then new articles are posted on their respective website waiting to be fetched (https://www.allocine.fr/) (https://screenrant.com/).

In term of database we use MongoDB (https://www.mongodb.com/), Elasticsearch (https://www.elastic.co/) and as we said before  HDFS (https://hadoop.apache.org/).
"""


import os

from feeds.twitterClient import TwitterClient
from feeds.tmdbClient import TMDbClient
from feeds.rssClient import RSSClient
from tools.elasticSearch import ElasticSearchClient
from tools.sentimentAnalysis import SentimentAnalysis
from dockers.app import DockerManager


TWITTER_MAX_FETCH = 100


def main():
    elasticSearchClient = ElasticSearchClient()
    sentimentAnalysis = SentimentAnalysis()

    rss_urls = {
        'allocinesemaine': 'http://rss.allocine.fr/ac/cine/cettesemaine',
        'allocineaffiche': 'http://rss.allocine.fr/ac/cine/alaffiche',
        'screenrant': 'https://screenrant.com/feed/',
    }

    os.chdir("/home/frantkich/Documents/Ynov/PizzaDB/dockers")
    dockerManager = DockerManager()
    dockerManager.start()

    tmdb_feed = TMDbClient()
    movie_id, movie_title = tmdb_feed.movieMenu()
    tmdb_feed.downloadPic(movie_id)

    # twitter_feed = TwitterClient(elasticSearchClient, sentimentAnalysis)
    # twitter_feed.setSupportedLanguages(sentimentAnalysis.supported_languages)
    # twitter_feed.pushNewTweets(query=movie_title, count=TWITTER_MAX_FETCH)

    # rss_feed = RSSClient(elasticSearchClient, sentimentAnalysis)
    # rss_feed.addSources(rss_urls)
    # rss_feed.pushNewArticles()
    
    #  Saving image on HDFS (commands in Dockerfile, restarting container since /images binded to /hadoop/dfs/data)
    dockerManager.createHDFSDirectory()
    dockerManager.reqToDocker('loadToHDFS')

if __name__ == '__main__':
    main()
