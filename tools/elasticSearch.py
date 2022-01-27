from elasticsearch import helpers, Elasticsearch, NotFoundError
from requests.exceptions import ConnectionError
from requests import get
from sys import platform
from time import sleep
import os

if platform == 'win32':
    ELASTIC_SEARCH_START = "C:\\Program Files\\elasticsearch-7.16.2\\bin\\elasticsearch.bat"
else:
    ELASTIC_SEARCH_START = 'systemctl restart elasticsearch.service'
MAX_RETRY=6

class ElasticSearchClient(object):
    def __init__(self):
        """ 
        DESC : badic init methode, initialize ES Client for later usage 
        """
        self.esClient = Elasticsearch()

    def start(self):
        """ 
        DESC : Launch the process
        OUT  : Returns True if it already exists, False if it don't
        """
        try:
            response = get("http://localhost:9200/")
        except ConnectionError:
            response = None
        if not(response):
            print("ElasticSearch Strating...")
            os.system(ELASTIC_SEARCH_START)
            count = 0
            while count <= MAX_RETRY:
                try: 
                    if get("http://localhost:9200/").status_code == 200:
                        print("\tElasticSearch started !\n")
                        break
                    else:
                        print("\tFailed to connect to ElasticSearch, next attempt in 5 seconds...\n")
                        sleep(5)
                        count += 1
                except ConnectionError:
                    pass
            if count == MAX_RETRY:
                print("\tFailed to connect to ElasticSearch Database, quiting.... !\n")
                quit()

    def ifExist(self, index, id):
        """ 
        DESC : Makes shure we don't insert the same row twice 

        IN   : index - the name of the Elasticsearch index
               newId - id from to search in Db
        OUT  : Returns True if it already exists, False if it don't
        """
        try:
            return self.esClient.get(index=index, id=id)
        except NotFoundError:
            return False

    def insertData(self, actions):
        """ 
        DESC : Insert a serie of document in the database in one request

        IN   : actions - array of dict containing the sorted infos
        OUT  : result of the request
        """
        return helpers.bulk(self.esClient, actions)

    def deleteData(self, index):
        """ 
        DESC : Delete every entires by index
        
        IN   : index - that will be used to find entries to be deleted
        OUT  : result of the request
        """
        return self.esClient.indices.delete(index=index, ignore=[400, 404])

    def clearAllCache(self):
        """ 
        DESC : Delete cache by index (list, comma separated)
        
        IN   : index - that will cache be cleared from
        OUT  : result of the request
        """
        return self.esClient.indices.clear_cache(self.esClient)

    def getData(self, query):
        return self.esClient.search(index='*', query={"query_string": {"query": query}}, size=1000)