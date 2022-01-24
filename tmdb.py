import tmdbsimple as tmdb
import requests
import os
from sys import platform

# importer liste de nouveautés
# choix d'un movie
# récupération et stockage de l'affiche dans HDFS

tmdb.API_KEY = '678b941591dc9bdb6ec1352563253fdd'
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()


# Argument : - name : name of the directory
# Test id directory exists in working directory, if not, creates it
def testDirOrCreate(name):
    if not (os.path.isdir(name)):
        path = os.path.join('\\', os.getcwd(), name)
        try:
            os.mkdir(path)
            print('./app/images directory created')
        except:
            print('Failed to create ./app/images directory,'
                  'please launch in administrator privileges')

# Argument : - movies : array
# Test id directory exists in working directory, if not, creates it
def movieMenu(movies):
    menu = 'List of available movies :\n'
    count = 1
    for movie in movies:
        menu = menu + str(count) + ' : ' + movie + '\n'
        count += 1
    return menu

# Clears console depending on operating system
def clearConsole():
    if platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


tmdbMovies = tmdb.Movies()
nowPlaying = tmdbMovies.now_playing()
movies = [movie['original_title'] for movie in nowPlaying['results']]
clearConsole()
print(movieMenu(movies))

testDirOrCreate('images')