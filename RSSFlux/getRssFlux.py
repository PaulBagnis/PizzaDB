import feedparser
from pymongo import MongoClient
import time
import ssl
import urllib

#  TO DO : Utiliser BeautifulSoup pour parse le HTML et récuperer que ce qui peut nous interesser
#          Passer sur ElasticSearch

client = MongoClient("localhost", 27017)
db = client.RSSFlux
allocine = db.allocine
screenrant = db.screenrant


urls = {
    "allocine": [
        "http://rss.allocine.fr/ac/cine/cettesemaine",
        "http://rss.allocine.fr/ac/cine/alaffiche",
    ],
    "screenrant": ["https://screenrant.com/feed/"],
}


def alreadyExists(col, newID):
    if len(list(db[col].find({"id": newID}, {"_id": 1}))) > 0:
        return True
    else:
        return False


def getArticlesFromRSS():
    for source in urls:
        nbOfNewArticles = 0
        for url in urls[source]:
            Feed = feedparser.parse(url)
            # Gestion des problèmes de certificats lors de la requête HTTP
            try :
                if isinstance(Feed.bozo_exception, urllib.error.URLError):
                    ssl._create_default_https_context = ssl._create_unverified_context
                    Feed = feedparser.parse(url)
            except :
                continue
            articles = []
            for entry in Feed.entries:
                if alreadyExists(source, entry["id"]):
                    break
                articles.append(entry)
            if articles:
                db[source].insert_many(articles)
                nbOfNewArticles += len(articles)
        print(
            "{} new articles added in RSSFlux.{} collection !".format(
                nbOfNewArticles, source
            )
        )


getArticlesFromRSS()
