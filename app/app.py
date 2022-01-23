import tmdbsimple as tmdb
import requests
import os
from sys import platform
from alphabet_detector import AlphabetDetector
import docker

# récupération et stockage de l'affiche dans HDFS

tmdb.API_KEY = '678b941591dc9bdb6ec1352563253fdd'
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()
clearSyntaxe = 'cls' if platform == 'win32' else 'clear'
ad = AlphabetDetector()

# Argument : - container_name: the name of the container
# Verify the status of a container by it's name, return True if running
def is_container_running(container_name: str):
    RUNNING = "running"
    docker_client = docker.from_env()

    try:
        container = docker_client.containers.get(container_name)
    except docker.errors.NotFound as exc:
        print(f"Check container name!\n{exc.explanation}")
        return False
    else:
        container_state = container.attrs["State"]
        return container_state["Status"] == RUNNING


# Argument : - name : name of the directory
# Test id directory exists in working directory, if not, creates it
def testDirOrCreate(name):
    if not (os.path.isdir(name)):
        path = os.path.join('\\', os.getcwd(), name)
        try:
            os.mkdir(path)
            print('./app/images directory created')
        except:
            print(
                'Failed to create ./app/images directory, please launch in administrator privileges'
            )

# Argument : - movies : array
# Test id directory exists in working directory, if not, creates it
def movieMenu(movies):
    menu = '\n\n\tList of available movies :\n\n'
    count = 1
    for movie in movies:
        menu = menu + '\t' + str(count) + ' : ' + movie + '\n'
        count += 1
    return menu, count


# Argument : - inputMessage : message for input function
#            - menu : return value from movieMenu()
# Prints menu and returns input messages
def printMenu(inputMessage, menu):
    print(menu[0])
    return input(inputMessage)



tmdbMovies = tmdb.Movies()
# print([method_name for method_name in dir(tmdbMovies) if callable(getattr(tmdbMovies, method_name))])
# test = input('ok ?')
nowPlaying = tmdbMovies.now_playing()
movies = [movie['original_title'] for movie in nowPlaying['results'] if ad.only_alphabet_chars(movie['original_title'], 'LATIN')]

# User choice of movie in console
os.system(clearSyntaxe)
menu = movieMenu(movies)
movieChoice = printMenu('\tWhat movie do you want info on ?\n\tPlease enter movie number : ', menu)
# Test if choice is valid
while True :
    try :
        if 1 <= int(movieChoice) <= menu[1] :
            break
        else :
            os.system(clearSyntaxe)
            movieChoice = printMenu('\tWhat movie do you want info on ?\n\tPlease enter movie number (an existing one this time) : ', menu)
    except ValueError :
        os.system(clearSyntaxe)
        movieChoice = printMenu('\tWhat movie do you want info on ?\n\tPlease enter movie number (an existing one this time) : ', menu)

# Query film's image and save it /images directory
os.system(clearSyntaxe)
currentMovie = tmdb.Movies(nowPlaying['results'][int(movieChoice)]['id'])
imgUrl = 'https://www.themoviedb.org/t/p/w150_and_h225_bestv2' + currentMovie.info()['poster_path']
imgPath = os.path.join('\\', os.path.join('\\', os.getcwd(), 'images'), currentMovie.info()['original_title'] + '.jpg')

with open(imgPath, 'wb') as handle:
    response = requests.get(imgUrl, stream=True)
    if not response.ok:
        print('Failed to get image from Movie. Please try again ¯\_(ツ)_/¯')
    for block in response.iter_content(1024):
        if not block:
            break
        handle.write(block)

# Saving image on HDFS





testDirOrCreate('images')
