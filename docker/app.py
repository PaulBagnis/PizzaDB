import tmdbsimple as tmdb
import requests
import os
from sys import platform
from alphabet_detector import AlphabetDetector
import docker
import time


tmdb.API_KEY = '678b941591dc9bdb6ec1352563253fdd'
tmdb.REQUESTS_TIMEOUT = 10
tmdb.REQUESTS_SESSION = requests.Session()

CLEAR_SYNTAXE = 'cls' if platform == 'win32' else 'clear'


tmdbMovies = tmdb.Movies()
# dockerClient = docker.from_env()


def isContainerRunning(container_name):
    """
    DESC : check if container is running

    IN   : container_name - the name of the container
    OUT  : return True if it's running, else False
    """
    try:
        return dockerClient.inspect_container(container_name)['State']['Status'] == 'running'
    except Exception as e:
        print('Error func: isContainerRunning() -> {}'.format(e))
        return False

### REVIEW
def isDockerRunning(dockerComposeCommand='docker-compose up -d', restart=False):
    """
    DESC : Check if docker and Hadoop image are running

    IN   : dockerComposeCommand - command to execute to check (default: docker-compose up -d)
    OUT  : return True if it's running, else False
    """
    dockerCompose = False
    while True:
        try:
            if not(dockerCompose) or restart:
                os.system(dockerComposeCommand)
                dockerCompose, restart == True, False
            if isContainerRunning('datanode'):
                break
        except:
            print('{}\n\n\tPlease run docker before lauching program\n\n'.format(isContainerRunning('datanode')))
            quit()
        time.sleep(5)


def testDirOrCreate(name):
    """
    DESC : Test id directory exists in working directory, if not, creates it

    IN   : name - directory's name
    """
    if not os.path.isdir(name):
        path = os.path.join('\\', os.getcwd(), name)
        try:
            os.mkdir(path)
            print('./app/images directory created')
        except:
            print('Failed to create ./app/images directory, please launch in administrator privileges')


def movieMenu(movies, warning=''):
    """
    DESC : Display a list of movies to choose from

    IN   : movies - list to be displayed
           warning - an additionnal str to warn wrong inputs (default is null)
    OUT  : the position of the choosen movie
    """
    os.system(CLEAR_SYNTAXE)
    print('\n\n\tList of available movies :\n\n'
          '\n'.join('\t{} : {}'.format(p, title) for p, title in enumerate(movies)))
    return int(input('What movie do you want info on ?\n{} > '.format(warning)))


def reqToDocker(url):
    """
    DESC : send request to the docker API

    IN   : url - endpoint
    """
    if requests.get(url) == '256': 
        print('\tZEPARTIIII')
    else:
        print('\tSomething went wrong ¯\_(ツ)_/¯')


############################
#                          #
#      MAIN FUNCTION       #
#                          #
############################


# testDirOrCreate('images')
# isDockerRunning(False)


nowPlaying = tmdbMovies.now_playing()
movies = [movie['original_title'] for movie in nowPlaying['results'] if AlphabetDetector().only_alphabet_chars(movie['original_title'], 'LATIN')]


movieChoice = movieMenu(movies)
# Test if choice is an Integer in the range of the menu
while 1 <= movieChoice <= len(movies):
    movieChoice = movieMenu(movies, '( An existing one this time )\n')


# Query film's image and save it /images directory
movieId=nowPlaying['results'][movieChoice]['id']
imgUrl = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2'+tmdb.Movies(movieId).info()['poster_path']
imgPath = os.path.join(os.getcwd(), 'images', str(movieId) + '.jpg')

if not os.path.exists(imgPath):
    with open(imgPath, 'wb') as file:
        response = requests.get(imgUrl, stream=True)
        if not response.ok:
            print('Failed to get image from Movie. Please try again ¯\_(ツ)_/¯')
        for block in response.iter_content(1024):
            if not block:
                break
            file.write(block)

#  Saving image on HDFS (commands in Dockerfile, restarting container since /images binded to /hadoop/dfs/data)
# print('\n\n\tCreating HDFS directory\n')
# reqToDocker('http://localhost:5000/createHDFSDir')

# print('\n\n\tLoading to HDFS\n')
# reqToDocker('http://localhost:5000/loadToHDFS')

