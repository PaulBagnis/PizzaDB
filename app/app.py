import tmdbsimple as tmdb
import requests
import os
from sys import platform
from alphabet_detector import AlphabetDetector
import docker
import time
# récupération et stockage de l'affiche dans HDFS

tmdb.API_KEY = "678b941591dc9bdb6ec1352563253fdd"
tmdb.REQUESTS_TIMEOUT = 10
tmdb.REQUESTS_SESSION = requests.Session()
clearSyntaxe = "cls" if platform == "win32" else "clear"
ad = AlphabetDetector()
dockerClient = docker.from_env()


# Argument : - container_name: the name of the container
# Verify the status of a container by it's name, return True if running
def isContainerRunning(containerName: str):
    try :
        if dockerClient.inspect_container(containerName)['State']['Status'] == 'running':
            return True
        else :
            return False
    except:
        return False


# Check if docker is running and Hadoop image too, or crash
def isDockerRunning(dockerComposeCommand, restart=False):
    dockerCompose = False
    while True:
        try:
            dockerStatus = isContainerRunning("datanode")
            if not(dockerCompose) or restart:
                os.system(dockerComposeCommand)
                dockerCompose, restart == True, False
            if dockerStatus:
                break
        except:
            print(isContainerRunning("datanode"))
            print("\n\n\tPlease run docker before lauching program\n\n")
            quit()
        time.sleep(5)


# Argument : - name : name of the directory
# Test id directory exists in working directory, if not, creates it
def testDirOrCreate(name):
    if not (os.path.isdir(name)):
        path = os.path.join("\\", os.getcwd(), name)
        try:
            os.mkdir(path)
            print("./app/images directory created")
        except:
            print(
                "Failed to create ./app/images directory, please launch in administrator privileges"
            )


# Argument : - movies : array
# Test id directory exists in working directory, if not, creates it
def movieMenu(movies):
    menu = "\n\n\tList of available movies :\n\n"
    count = 1
    for movie in movies:
        menu = menu + "\t" + str(count) + " : " + movie + "\n"
        count += 1
    return menu, count


# Argument : - inputMessage : message for input function
#            - menu : return value from movieMenu()
# Prints menu and returns input messages
def printMenu(inputMessage, menu):
    print(menu[0])
    return input(inputMessage)


############################
#                          #
#      MAIN FUNCTION       #
#                          #
############################

os.system(clearSyntaxe)

isDockerRunning("docker-compose up -d", False)

tmdbMovies = tmdb.Movies()
# print([method_name for method_name in dir(dockerClient.inspect_container('datanode')) if callable(getattr(dockerClient.inspect_container('datanode'), method_name))])
# test = input('ok ?')
nowPlaying = tmdbMovies.now_playing()
movies = [
    movie["original_title"]
    for movie in nowPlaying["results"]
    if ad.only_alphabet_chars(movie["original_title"], "LATIN")
]

# User choice of movie in console
os.system(clearSyntaxe)
menu = movieMenu(movies)
movieChoice = printMenu(
    "\tWhat movie do you want info on ?\n\tPlease enter movie number : ", menu
)
# Test if choice is an Integer in the range of the menu
while True:
    try:
        if 1 <= int(movieChoice) <= menu[1]:
            break
        else:
            os.system(clearSyntaxe)
            movieChoice = printMenu(
                "\tWhat movie do you want info on ?\n\tPlease enter movie number (an existing one this time) : ",
                menu,
            )
    except ValueError:
        os.system(clearSyntaxe)
        movieChoice = printMenu(
            "\tWhat movie do you want info on ?\n\tPlease enter movie number (an existing one this time) : ",
            menu,
        )

# Query film's image and save it /images directory
testDirOrCreate("images")
os.system(clearSyntaxe)
currentMovie = tmdb.Movies(nowPlaying["results"][int(movieChoice)-1]["id"])
imgUrl = (
    "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
    + currentMovie.info()["poster_path"]
)
imgPath = os.path.join(
    "\\",
    os.path.join("\\", os.getcwd(), "images"),
    str(nowPlaying["results"][int(movieChoice)-1]["id"]) + ".jpg",
)

if not(os.path.exists(imgPath)):
    with open(imgPath, "wb") as handle:
        response = requests.get(imgUrl, stream=True)
        if not response.ok:
            print("Failed to get image from Movie. Please try again ¯\_(ツ)_/¯")
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

#  Saving image on HDFS (commands in Dockerfile, restarting container since /images binded to /hadoop/dfs/data)
print('\n\n\tCreating HDFS directory\n\n')
response = requests.get("http://localhost:5000/createHDFSDir")
print(response)

print('\n\n\tLoading to HDFS\n\n')
response = requests.get("http://localhost:5000/loadToHDFS")
print(response)
test=input('ok ?')
# NON

# print([method_name for method_name in dir(dockerClient) if callable(getattr(dockerClient, method_name))])
# containerImage = dockerClient.containers.get('datanode')['Config']['Image']
# print(dockerClient.get_image())
# isDockerRunning("docker-compose up --build -d", True)