import feedparser
import ssl
import urllib
from elasticsearch import Elasticsearch, exceptions, helpers
from bs4 import BeautifulSoup

# ElasticSearch client instantiation
es = Elasticsearch()

# RSS feed's urls
urls = {
    "allocinesemaine": ["http://rss.allocine.fr/ac/cine/cettesemaine"],
    "allocineaffiche": ["http://rss.allocine.fr/ac/cine/alaffiche"],
    "screenrant": ["https://screenrant.com/feed/"],
}


# Argument : - ind : the name of the Elasticsearch index
#            - newId : id from the RSS article to search in Db
# Returns True if Article already exists in ElastcSearch index, False if don't
# Makes shure we don't insert the same article twice
def alreadyExists(ind, newID):
    query_body = {"bool": {"must": {"match": {"id": newID}}}}
    try:
        return es.search(index=ind, query=query_body)["hits"]["total"]["value"]
    # This Error is raised when index doesn't exists so function will return False
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


# Argument : - content : content from article that contains HTML
# Returns only the main text from article without any HTML tag
def parsingHtml(content):
    return BeautifulSoup(content, "lxml").find_all("p")[0].text.split(" - ")[1]


# Argument : - source : name of the index
#            - articles : array of RSS articles to insert in DB
# Does the bulk inserts in ElasticSearch DB
def insertInDb(source, articles):
    actions = []
    for article in articles:
        # Test if article is in HTML format, if yes, parses via parsingHtml function
        if bool(BeautifulSoup(article["summary"], "html.parser").find()):
            article["summary"] = parsingHtml(article["summary"])
        actions.append({
            "_index": source,
            "_source": {
                "title": article["title"],
                "summary": article["summary"],
                "published": article["published_parsed"],
                "id": article["id"],
            },
        })
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
        print("{} new articles added in {}'s index !".format(nbOfNewArticles, source))


# Uncomment to delete indexes
# es.indices.delete(index="allocinesemaine", ignore=[400, 404])
# es.indices.delete(index="allocineaffiche", ignore=[400, 404])
# es.indices.delete(index="screenrant", ignore=[400, 404])
getArticlesFromRSS()
