
from feeds.twitterClient import TwitterClient
from feeds.tmdbClient import TMDbClient
from feeds.rssClient import RSSClient
from tools.elasticSearch import ElasticSearchClient
from dockers.app import DockerManager

from sys import platform
import os


def reset():
    elasticSearchClient = ElasticSearchClient()
    elasticSearchClient.start()

    TwitterClient(elasticSearchClient).deleteDb()
    RSSClient(elasticSearchClient, urls={'allocinesemaine': '','allocineaffiche': '','screenrant': '',}).deleteDb()
    TMDbClient().deletePicDir()


    os.chdir("./dockers")
    dockerManager = DockerManager()
    os.chdir("../")
    dockerManager.start(True)
    dockerManager.deleteHDFSDirectory()
    

if __name__ == '__main__':
    reset()

