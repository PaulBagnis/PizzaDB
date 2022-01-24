#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
__authors__ = ("Guern Francois", "Bagnis Paul", "Takoutsink Jerry")
__email__ = ("francois.guern@ynov.com", "paul.bagnis@ynov.com", "jerry.takoutsing@ynov.com")
__copyright__ = "MIT"
__date__ = "2022-01-28"
__version__= "0.1.0"
__status__ = "Devlopement"
# ---------------------------------------------------------------------------
""" Details about the module and for what purpose it was built for """
# ---------------------------------------------------------------------------
from tools.elasticSearch import ElasticSearchClient
from tools.sentimentAnalysis import SentimentAnalysis
from feeds.twitterClient import TwitterClient
from feeds.rssClient import RSSClient
# ---------------------------------------------------------------------------


def main():
    es = ElasticSearchClient()
    sa = SentimentAnalysis()

    rss_urls = {
        'allocinesemaine': 'http://rss.allocine.fr/ac/cine/cettesemaine',
        'allocineaffiche': 'http://rss.allocine.fr/ac/cine/alaffiche',
        'screenrant': 'https://screenrant.com/feed/',
    }

    rss_feed = RSSClient(es, sa)
    rss_feed.addSources(rss_urls)
    rss_feed.deleteDb()
    rss_feed.pushNewArticles()

    twitter_feed = TwitterClient(es, sa)
    twitter_feed.setSupportedLanguages(sa.supported_languages)
    twitter_feed.deleteDb()
    twitter_feed.pushNewTweets(query='movies', count=100)


if __name__ == '__main__':
    main()
