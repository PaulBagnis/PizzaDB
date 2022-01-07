import feedparser
from pymongo import MongoClient
import json

# url actu ciné : http://rss.allocine.fr/ac/actualites/cine
# url nouvelle sorties semaine : http://rss.allocine.fr/ac/cine/cettesemaine
# url film a l'affiche : http://rss.allocine.fr/ac/cine/alaffiche

client = MongoClient('localhost', 27017)
db = client.RSSFlux
allocine = db.allocine

urls = {
    "actualitescine" : "http://rss.allocine.fr/ac/actualites/cine",
    "cinecettesemaine" : "http://rss.allocine.fr/ac/cine/cettesemaine",
    "cinealaffiche" : "http://rss.allocine.fr/ac/cine/alaffiche"
}

def alreadyExists(newID):
    if len(list(allocine.find({'id': newID}, {'_id' : 1}))) > 0:
        return True
    else:
        return False

for key in urls :
    Feed = feedparser.parse(urls[key])
    articles = []
    for entry in Feed.entries : 
        
        if alreadyExists(entry["id"]) :
            break
        articles.append(entry)
    if articles : allocine.insert_many(articles)
