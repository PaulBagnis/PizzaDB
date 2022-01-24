from urllib.error import URLError
from bs4 import BeautifulSoup
from feedparser import parse
import ssl


class RSSClient(object):
    def __init__(self, db, sa, urls={}):
        """ 
        DESC :

        IN   :  
        OUT  : 
        """
        self.db = db
        self.sa = sa
        self.urls = urls

    
    def getFeed(self, url):
        """ 
        DESC :

        IN   :  - url : endpoint of the RSS feed we are going to fetch
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
        DESC :

        IN   :  
        OUT  : 
        """
        self.urls.update(urls)

    def insertDb(self, source, articles):
        """ 
        DESC : Does bulk inserts in ElasticSearch DB

        IN   : source - name of the index
               articles - array of RSS articles to insert in DB
        OUT  : 
        """
        actions = []
        for article in articles:
            # Test if article is in HTML format, if yes, parses via parsingHtml function
            if BeautifulSoup(article['summary'], 'html.parser').find():
                article['summary'] = self.parsingHtml(article['summary'])
            actions.append({
                '_index': source,
                '_id': article['id'],
                '_source': {
                    'title': article['title'],
                    'text': article['summary'],
                    'polarity': self.sa.calculatePolarity_baseFive(article['summary']),
                    'date': article['published_parsed'],
                },
            })
        self.db.insertData(actions)

    def deleteDb(self):
        """ 
        DESC :

        IN   :  
        OUT  : 
        """
        for source, _ in self.urls.items():
            self.db.deleteData(source)

    def alreadyExists(self, index, newID):
        """ 
        DESC : Makes shure we don't insert the same article twice

        IN   : index - the name of the Elasticsearch index
               newId - id from the RSS article to search in Db
        OUT  : True if Article already exists in ElastcSearch index, False if don't
        """
        try:
            return self.db.ifExist(index, newID)['hits']['total']['value']
        except:
            return False

    def parsingHtml(self, content):
        """ 
        DESC : Returns only the main text from article without any HTML tag

        IN   : content - content from article that contains HTML
        OUT  : 
        """
        return BeautifulSoup(content, 'lxml').find_all('p')[0].text.split(' - ')[1]

    def getArticlesFromRSS(self):
        """ 
        DESC :  Main function, looping on RSS endpoints to fetch data and insert it in our ElasticSearch database
        IN   : 
        OUT  : 
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
        DESC :
        IN   :  
        OUT  : 
        """
        for source, articles in self.getArticlesFromRSS():
            self.insertDb(source, articles)
