from elasticsearch import helpers, Elasticsearch, NotFoundError


class ElasticSearchClient(object):
    def __init__(self):
        # ElasticSearch client instantiation
        self.esClient = Elasticsearch()

    # Argument : - index : the name of the Elasticsearch index
    #            - newId : id from the RSS article to search in Db
    # Returns True if Article already exists in ElastcSearch index, False if don't
    # Makes shure we don't insert the same article twice
    def ifExist(self, index, newID):
        try:
            return self.esClient.search(
                index=index, query={'bool': {'must': {'match': {'id': newID}}}}
            )
        # This Error is raised when index doesn't exists so function will return False
        except NotFoundError:
            return False

    def insertData(self, actions):
        return helpers.bulk(self.esClient, actions)

    def deleteData(self, index):
        return self.esClient.indices.delete(index=index, ignore=[400, 404])
