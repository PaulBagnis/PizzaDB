from databases.elasticSearch import ElasticSearchClient
from rssFlux.rssFeedClient import RSSFeedClient
from botTwitter.twitterClient import TwitterClient
from sentimentAnalysis.sentimentAnalysis import SentimentAnalysis

def main():
    es = ElasticSearchClient()
    sa = SentimentAnalysis()

    # rss_urls = {
    #     'allocinesemaine': 'http://rss.allocine.fr/ac/cine/cettesemaine',
    #     'allocineaffiche': 'http://rss.allocine.fr/ac/cine/alaffiche',
    #     'screenrant': 'https://screenrant.com/feed/',
    # }

    # rss_feed = RSSFeedClient(es, sa)
    # rss_feed.addSources(rss_urls)
    # rss_feed.deleteDb()
    # rss_feed.pushNewArticles()

    twitter_feed = TwitterClient(es, sa)
    twitter_feed.setSupportedLanguages(['es', 'pt', 'it', 'fr', 'de', 'en'])
    twitter_feed.deleteDb()
    twitter_feed.pushNewTweets(query = 'Dune', count = 100)


if __name__ == '__main__':
    main()