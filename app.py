from databases.elasticSearch import ElasticSearchClient
from rssFlux.rssFeedClient import RSSFeedClient
from botTwitter.twitterClient import TwitterClient
from sentimentAnalysis.sentimentAnalysis import SentimentAnalysis

def percentage(part,whole):
    return format(100 * float(part)/float(whole), '.1f')

def main():
    rss_urls = {
        'allocinesemaine': 'http://rss.allocine.fr/ac/cine/cettesemaine',
        'allocineaffiche': 'http://rss.allocine.fr/ac/cine/alaffiche',
        'screenrant': 'https://screenrant.com/feed/',
    }

    hashtag='titanfall2'
    tweet_query_nb=300

    es = ElasticSearchClient()
    sa = SentimentAnalysis()
    rss_feed = RSSFeedClient(es, sa)
    rss_feed.addSources(rss_urls)
    rss_feed.deleteDb()
    rss_feed.pushNewArticles()

    # twitter_feed = TwitterClient(es, sa)
    # tweets = twitter_feed.get_tweets(query = hashtag, count = tweet_query_nb)

if __name__ == '__main__':
    main()