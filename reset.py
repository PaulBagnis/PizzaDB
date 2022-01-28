imagesName=('dockers_datanode:latest', 'bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8', 'bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8', 'bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8', 'bde2020/hadoop-historyserver:2.0.0-hadoop3.2.1-java8', 'bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8')
containerName=('datanode', 'historyserver', 'namenode', 'nodemanager', 'resourcemanager')
sources={'allocinesemaine': '','allocineaffiche': '','screenrant': ''}

from pymongo import MongoClient
from feeds.twitterClient import TwitterClient
from feeds.tmdbClient import TMDbClient
from feeds.rssClient import RSSClient
from tools.elasticSearch import ElasticSearchClient
from dockers.app import DockerManager
import pickledb


def reset():
    db_pickle = pickledb.load('project.db', False) 
    db_pickle.set('api_key', 'lQQaJPtSdyKab6zyi03lHSanu') 
    db_pickle.set('api_key_secret', 'texLfA0KI0VW428WMiPW5motO0z8PURFKvrJz0amktmGd0c3yK') 
    db_pickle.set('access_token', '1377622154683019265-RnmvsG8dt06VAdOvlcHhEaYZs6lVD0') 
    db_pickle.set('access_token_secret', 'SvWonpPDxsE3hNUfj2lrPjEvGb2Xj61tiJMWon0EKdEeg')
    elasticSearchClient = ElasticSearchClient()
    elasticSearchClient.start()

    TwitterClient(elasticSearchClient, db_pickle).deleteDb()
    RSSClient(elasticSearchClient, urls=sources).deleteDb()
    TMDbClient().deletePicDir()
    monog = MongoClient('localhost', 27017)
    monog.db.projetBDD.drop()
    monog.db.projetBDD.create_index('title')


    dockerManager = DockerManager()
    dockerManager.start(1, 'dockers')
    dockerManager.deleteHDFSDirectory()
    dockerManager.removeContainers(containerName)
    dockerManager.removeImages(imagesName)
    # dockerManager.start(1, 'dockers')
    

if __name__ == '__main__':
    reset()

