import feedparser
import ssl
import urllib
from elasticsearch import Elasticsearch, exceptions, helpers


#  TO DO : Utiliser BeautifulSoup pour parse le HTML et récuperer que ce qui peut nous interesser

# ElasticSearch client instantiation
es = Elasticsearch()


# RSS feed's urls
urls = {
    "allocine": [
        "http://rss.allocine.fr/ac/cine/cettesemaine",
        "http://rss.allocine.fr/ac/cine/alaffiche",
    ],
    "screenrant": ["https://screenrant.com/feed/"],
}


# Argument : - ind : the name of the Elasticsearch index
#            - newId : id from the RSS article to search in Db
# Returns True if Article already exists in ElastcSearch index, False if don't
# Makes shure we don't insert the same article twice
def alreadyExists(ind, newID):
    query_body = {"bool": {"must": {"match": {"id": newID}}}}
    try:
        res = es.search(index=ind, query=query_body)
        if res["took"] != 0:
            return True
        else:
            return False
    except exceptions.NotFoundError:
        return False


# Argument : - url : endpoint of the RSS feed we are going to fetch
# Returns the RSS feed and handles certificates problems when fetching feed
def getFeed(url):
    feed = feedparser.parse(url)
    try:
        if isinstance(feed.bozo_exception, urllib.error.URLError):
            ssl._create_default_https_context = ssl._create_unverified_context
            feed = feedparser.parse(url)
    except:
        pass
    return feed


# Argument : - source : name of the index
#            - articles : array of RSS articles to insert in DB
# Does the bulk inserts in ElasticSearch DB
def insertInDb(source, articles):
    actions = [{"_index": source, "_source": article} for article in articles]
    helpers.bulk(es, actions)


# Main function, looping on RSS endpoints to fetch data and insert it in our ElasticSearch database
def getArticlesFromRSS():
    for source in urls:
        nbOfNewArticles = 0
        for url in urls[source]:
            feed = getFeed(url)
            articles = []
            for entry in feed.entries:
                if alreadyExists(source, entry["id"]):
                    break
                articles.append(entry)
            if articles:
                insertInDb(source, articles)
                nbOfNewArticles += len(articles)
        print(
            "{} new articles added in RSSFlux.{} index !".format(
                nbOfNewArticles, source
            )
        )


getArticlesFromRSS()
