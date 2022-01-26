from urllib.error import URLError
from bs4 import BeautifulSoup
from feedparser import parse
import ssl


class RSSClient(object):
    def __init__(self, db, sentimentModule=None, urls={}):
        """ 
        DESC : basic init function

        IN   :  db - database where infos are going to be saved
                sentimentModule - sentiment analysis module analyse our string
                urls - sources where infos are going to be fetched
        """
        self.db = db
        self.sa = sentimentModule
        self.urls = urls
  
    def getFeed(self, url):
        """ 
        DESC : connect to the rss feed and return full data

        IN   : url - endpoint of the RSS feed we are going to fetch
        OUT  : json containing RSS feed infos
        """
        feed = parse(url)
        try:
            if isinstance(feed.bozo_exception, URLError):
                ssl._create_default_https_context = ssl._create_unverified_context
                feed = parse(url)
        except:
            pass
        return feed

    def addSources(self, urls):
        """ 
        DESC : simple function to add new RSS sources 

        IN   : urls - array of dictionnaries with sourcename and url 
        """
        self.urls.update(urls)

    def insertDb(self, source, articles):
        """ 
        DESC : create a array of dict then send them to the ElasticSearch DB

        IN   : source - name of the index
               articles - array of RSS articles to insert in DB
        """
        actions = []
        for article in articles:
            pol = self.sa.calculatePolarity_baseFive(article['summary']) if self.sa else 'n/a'
            # Test if article is in HTML format, if yes, parses via parsingHtml function
            if BeautifulSoup(article['summary'], 'html.parser').find():
                article['summary'] = self.parsingHtml(article['summary'])
            actions.append({
                '_index': source,
                '_id': article['id'],
                '_source': {
                    'title': article['title'],
                    'text': article['summary'],
                    'polarity': pol,
                    'date': article['published_parsed'],
                },
            })
        self.db.insertData(actions)

    def deleteDb(self):
        """ 
        DESC : ask the ElasticSearch db to delete every entries that as the same source as this function 
        """
        for source, _ in self.urls.items():
            self.db.deleteData(source)

    def alreadyExists(self, index, newID):
        """ 
        DESC : Makes shure we don't insert the same article twice

        IN   : index - the name of the Elasticsearch index
               newId - id from the RSS article to search in Db
        OUT  : True if the article already exist, False if it don't
        """
        try:
            return self.db.ifExist(index, newID)['hits']['total']['value']
        except:
            return False

    def parsingHtml(self, content):
        """ 
        DESC : Returns only the main text from article without any HTML tag

        IN   : content - HTML content
        OUT  : raw text
        """
        return BeautifulSoup(content, 'lxml').find_all('p')[0].text.split(' - ')[1]

    def getArticlesFromRSS(self):
        """ 
        DESC : looping on RSS endpoints to fetch data
        
        OUT  : array of dict containing RSS sources's datas 
        """
        feed = []
        for source, url in self.urls.items():
            nbOfNewArticles = 0
            articles = []
            for entry in self.getFeed(url).entries:
                if self.alreadyExists(source, entry['id']):
                    break
                articles.append(entry)
            if articles:
                nbOfNewArticles += len(articles)
                print('{} new articles added in {}\'s index !'.format(nbOfNewArticles, source))
                feed.append((source, articles))
            else:
                print('No new article found in {}\'s index !'.format(source))
        return feed

    def pushNewArticles(self):
        """ 
        DESC : Main function, that get RSS data before sending them to the DB 
        """
        for source, articles in self.getArticlesFromRSS():
            self.insertDb(source, articles)
