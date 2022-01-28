#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__authors__ = ("Guern Francois", "Bagnis Paul", "Takoutsink Jerry")
__email__ = ("francois.guern@ynov.com", "paul.bagnis@ynov.com", "jerry.takoutsing@ynov.com")
__copyright__ = "MIT"
__date__ = "2022-01-28"
__version__= "0.1.0"
__status__ = "Development"

"""
This project was developed to practice notions view in class mainly about database paradigms.
The contrains were to use different sources of data, in at least two different languages. 
We also had to use different databases with their own paradigms. 
Lastly we had to set up HDFS in any ways.

We decided to focuse on movies on this project, the reasons : a lot of free data online.
We choose to use 3 differents feeds:
TMDB -> The movie DataBase provide an API to fetch any data they had (https://www.themoviedb.org/).
Twitter -> The social media give access to every messages posted on their website (https://twitter.com/).
NewRSS -> Every now and then new articles are posted on their respective website waiting to be fetched (https://www.allocine.fr/) (https://screenrant.com/).

In term of database we use MongoDB (https://www.mongodb.com/), Elasticsearch (https://www.elastic.co/) and as we said before  HDFS (https://hadoop.apache.org/).
"""


import numpy
from pymongo import MongoClient
from sys import platform
import os

from feeds.tmdbClient import TMDbClient
from tools.elasticSearch import ElasticSearchClient
from dockers.app import DockerManager

CLEAR_SYNTAXE = 'cls' if platform == 'win32' else 'clear'


def main():
    elasticSearchClient = ElasticSearchClient()

    dockerManager = DockerManager()
    dockerManager.start(1, 'dockers')

    tmdb_feed = TMDbClient()
    input('ENTER')
    os.system(CLEAR_SYNTAXE)
    movie_id, movie_title, movie_notation = tmdb_feed.movieMenu()
    #  Saving image on HDFS (commands in Dockerfile, restarting container since /images binded to /hadoop/dfs/data)
    dockerManager.pullHDFS(movie_id, movie_title)

    # polarity mean by source
    data = elasticSearchClient.getData(movie_title)['hits']['hits']
    polarities={'tmdb': movie_notation}
    input('ENTER')
    os.system(CLEAR_SYNTAXE)
    if data:
        for hit in data:
            if not hit['_index'] in polarities:
                polarities[hit['_index']]=[hit['_source']['polarity']]
            else:
                polarities[hit['_index']].append(hit['_source']['polarity'])
        print('Calculating polarity of sources...')
        for key, value in polarities.items():
            polarities[key] = format(numpy.array(value).mean(), '.1f')
            print('{} : {}'.format(key, polarities[key]))
        print('{}.jpg'.format(movie_title))

    client = MongoClient('localhost', 27017)# Create new index
    client.db.projetBDD.insert_one({
        '_id': movie_id,
        'title': movie_title,
        'polaritiesSource': polarities,
        'path_pic': '{}.jpg'.format(movie_id)
    })

if __name__ == '__main__':
    main()
