from feedparser import parse
from  urllib.error import URLError
from bs4 import BeautifulSoup
import ssl


class RSSFeedClient(object):
    def __init__(self, db, urls):
        self.db=db
        self.urls=urls

    # Argument : - url : endpoint of the RSS feed we are going to fetch
    # Returns the RSS feed and handles certificates problems when fetching feed
    def getFeed(self, url):
        feed = parse(url)
        try:
            if isinstance(feed.bozo_exception, URLError):
                ssl._create_default_https_context = ssl._create_unverified_context
                feed = parse(url)
        except:
            pass
        return feed


    # Argument : - source : name of the index
    #            - articles : array of RSS articles to insert in DB
    # Does the bulk inserts in ElasticSearch DB
    def insertDb(self, source, articles):
        actions = []
        for article in articles:
            # Test if article is in HTML format, if yes, parses via parsingHtml function
            if bool(BeautifulSoup(article['summary'], 'html.parser').find()):
                article['summary'] = self.parsingHtml(article['summary'])
            actions.append({
                '_index': source,
                '_source': {
                    'title': article['title'],
                    'summary': article['summary'],
                    'published': article['published_parsed'],
                    'id': article['id'],
                }
            })
        self.db.insertData(actions)

    def deleteDb(self):
        for source, url in self.urls.items():
            self.db.deleteData(source)


    # Argument : - index : the name of the Elasticsearch index
    #            - newId : id from the RSS article to search in Db
    # Returns True if Article already exists in ElastcSearch index, False if don't
    # Makes shure we don't insert the same article twice
    def alreadyExists(self, index, newID):
        try:
            return self.db.ifExist(index, newID)['hits']['total']['value']
        except :
            return False

            
    # Argument : - content : content from article that contains HTML
    # Returns only the main text from article without any HTML tag
    def parsingHtml(self, content):
        return BeautifulSoup(content, 'lxml').find_all('p')[0].text.split(' - ')[1]


    # Main function, looping on RSS endpoints to fetch data and insert it in our ElasticSearch database
    def getArticlesFromRSS(self):
        feed=[]
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
        for source, articles in self.getArticlesFromRSS():
            self.insertDb(source, articles)


