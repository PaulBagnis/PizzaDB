
from feeds.twitterClient import TwitterClient
from feeds.tmdbClient import TMDbClient
from feeds.rssClient import RSSClient
from tools.elasticSearch import ElasticSearchClient
from dockers.app import DockerManager


def reset():
    elasticSearchClient = ElasticSearchClient()
    elasticSearchClient.start()

    TwitterClient(elasticSearchClient).deleteDb()
    RSSClient(elasticSearchClient, urls={'allocinesemaine': '','allocineaffiche': '','screenrant': '',}).deleteDb()
    TMDbClient().deletePicDir()


    dockerManager = DockerManager()
    dockerManager.removeContainers(('datanode', 'historyserver', 'namenode', 'nodemanager', 'resourcemanager'))
    dockerManager.removeImages(('dockers_datanode:latest', 
                                'bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8',
                                'bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8',
                                'bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8',
                                'bde2020/hadoop-historyserver:2.0.0-hadoop3.2.1-java8',
                                'bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8',
    ))
    dockerManager.start(1, 'dockers')
    dockerManager.deleteHDFSDirectory()
    

if __name__ == '__main__':
    reset()

