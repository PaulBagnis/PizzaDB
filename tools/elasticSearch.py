from elasticsearch import helpers, Elasticsearch, NotFoundError


class ElasticSearchClient(object):
    def __init__(self):
        """ 
        DESC : badic init methode, initialize ES Client for later usage 
        """
        self.esClient = Elasticsearch()

    def ifExist(self, index, newID):
        """ 
        DESC : Makes shure we don't insert the same row twice 

        IN   : index - the name of the Elasticsearch index
               newId - id from to search in Db
        OUT  : Returns True if it already exists, False if it don't
        """
        try:
            return self.esClient.search(
                index=index, query={'bool': {'must': {'match': {'id': newID}}}}
            )
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
