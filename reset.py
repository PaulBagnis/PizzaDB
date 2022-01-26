from dockers.app import DockerManager
from tools.elasticSearch import ElasticSearchClient
import os
from sys import platform
import time
import requests


PATH_TO_ELASTIC_SEARCH_BAT = (
    "C:\\Program Files\\elasticsearch-7.16.2\\bin\\elasticsearch.bat"
)
PATH_TO_MONGO_EXE = "C:\\Program Files\\MongoDB\\Server\\5.0\\bin\\mongod.exe"
CLEAR_SYNTAXE = "cls" if platform == "win32" else "clear"
MAX_RETRIES = 5

def startES():
    """
    DESC : Starts ElasticSearch Database and tries to clear cache to be shure database is running
    """
    os.startfile(os.path.normpath(PATH_TO_ELASTIC_SEARCH_BAT))
    count = 0
    while count <= MAX_RETRIES:
        try:
            response = requests.get("http://localhost:9200/")
            if response.status_code == 200:
                print("\tElasticSearch started !\n")
                break
            else:
                print("\tFailed to connect to ElasticSearch, next attempt in 10 seconds...\n")
                time.sleep(10)
                count += 1
        except requests.exceptions.ConnectionError :
            pass
    if count == MAX_RETRIES:
        print("\tFailed to connect to ElasticSearch Database, try again you sheep !\n")

def clearES():
    """
    DESC : Starts ElasticSearch Database and tries to clear cache to be shure database is running
           Once done, clears all indexes
    """
    response = None
    try:
        response = requests.get("http://localhost:9200/")
    except requests.exceptions.ConnectionError :
        pass
    if not(response):
        startES()
    es = ElasticSearchClient()
    es.deleteData("allocinesemaine")
    es.deleteData("allocinealaffiche")
    es.deleteData("screenrant")


os.system(CLEAR_SYNTAXE)

# launch docker
print("\t###############\n\tStarting Docker\n\t###############\n")
os.chdir("./dockers")
dockerManager = DockerManager()
dockerManager.isDockerRunning("docker-compose up --build -d", False)
dockerManager.deleteHDFSDirectory()

os.chdir("../")
print("\t######################\n\tDocker Started")

# Clear of ElasticSearch
print("\tClearing ElasticSearch\n\t######################\n")
clearES()
print("\t#####################\n\tElasticSearch Cleared\n\t#####################")


input('\n\tReset done. Press a key and type "python app.py" to enjoy app')
