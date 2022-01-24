from elasticsearch import helpers, Elasticsearch, NotFoundError


class ElasticSearchClient(object):
    def __init__(self):
        """ 
        DESC :
        IN   :  
        OUT  : 
        """
        self.esClient = Elasticsearch()

    def ifExist(self, index, newID):
        """ 
        DESC : Makes shure we don't insert the row

        IN   : index - the name of the Elasticsearch index
               newId - id from to search in Db
        OUT  : Returns True if it already exists in ElastcSearch index, False if don't
        """
        try:
            return self.esClient.search(
                index=index, query={'bool': {'must': {'match': {'id': newID}}}}
            )
        except NotFoundError:
            return False

    def insertData(self, actions):
        """ 
        DESC :
        IN   :  
        OUT  : 
        """
        return helpers.bulk(self.esClient, actions)

    def deleteData(self, index):
        """ 
        DESC :
        IN   :  
        OUT  : 
        """
        return self.esClient.indices.delete(index=index, ignore=[400, 404])
