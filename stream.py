from time import sleep
import pickledb
from feeds.twitterClient import TwitterClient
from feeds.tmdbClient import TMDbClient
from feeds.rssClient import RSSClient
from tools.elasticSearch import ElasticSearchClient
from tools.sentimentAnalysis import SentimentAnalysis
from dockers.app import DockerManager

TWITTER_MAX_FETCH = 50


def main():
    db_pickle = pickledb.load('project.db', False) 
    db_pickle.set('api_key', 'lQQaJPtSdyKab6zyi03lHSanu') 
    db_pickle.set('api_key_secret', 'texLfA0KI0VW428WMiPW5motO0z8PURFKvrJz0amktmGd0c3yK') 
    db_pickle.set('access_token', '1377622154683019265-RnmvsG8dt06VAdOvlcHhEaYZs6lVD0') 
    db_pickle.set('access_token_secret', 'SvWonpPDxsE3hNUfj2lrPjEvGb2Xj61tiJMWon0EKdEeg')
    elasticSearchClient = ElasticSearchClient()
    sentimentAnalysis = SentimentAnalysis()

    twitter_feed = TwitterClient(elasticSearchClient, db_pickle, 
    sentimentAnalysis)
    tmdb_feed = TMDbClient(elasticSearchClient)
    rss_feed = RSSClient(elasticSearchClient, sentimentAnalysis, {
        'allocinesemaine': 'http://rss.allocine.fr/ac/cine/cettesemaine',
        'allocineaffiche': 'http://rss.allocine.fr/ac/cine/alaffiche',
        'screenrant': 'https://screenrant.com/feed/',
    })

    dockerManager = DockerManager()
    dockerManager.start(1, 'dockers')

    while True:
        print('Start hour fetch !')
        rss_feed.pushNewArticles()
        for movie in tmdb_feed.fetchNewMovies():
            twitter_feed.pushNewTweets(query=movie['original_title'], count=TWITTER_MAX_FETCH)
            pic_path = tmdb_feed.downloadPic(movie['id'])
            dockerManager.createHDFSDirectory() 
            dockerManager.picToHDFS(pic_path)
        print('End hour fetch !')
        sleep(3600)

if __name__ == '__main__':
    main()
