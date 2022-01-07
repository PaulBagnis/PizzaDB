import feedparser
from pymongo import MongoClient
import time

client = MongoClient("localhost", 27017)
db = client.RSSFlux
allocine = db.allocine
screenrant = db.screenrant


urls = {
    "allocine": [
        "http://rss.allocine.fr/ac/actualites/cine",
        "http://rss.allocine.fr/ac/cine/cettesemaine",
        "http://rss.allocine.fr/ac/cine/alaffiche",
    ],
    "screenrant": ["https://screenrant.com/feed/"],
}


def alreadyExists(col, newID):
    query = col + ".find({'id': '" + newID + "'}, {'_id': 1})"
    response = eval(query)
    if len(list(response)) > 0:
        return True
    else:
        return False


def getArticlesFromRSS():
    while True:
        for source in urls:
            nbOfNewArticles = 0
            for url in urls[source]:
                Feed = feedparser.parse(url)
                articles = []
                for entry in Feed.entries:
                    if alreadyExists(source, entry["id"]):
                        break
                    articles.append(entry)
                if articles:
                    query = source + ".insert_many(articles)"
                    exec(query)
                    nbOfNewArticles += len(articles)
            print(
                "{} new articles added in RSSFlux.{} collection !".format(
                    nbOfNewArticles, source
                )
            )
        time.sleep(10)


getArticlesFromRSS()
