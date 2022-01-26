from dockers.app import DockerManager
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
                print(
                    "\tFailed to connect to ElasticSearch, next attempt in 10 seconds...\n"
                )
                time.sleep(10)
                count += 1
        except requests.exceptions.ConnectionError :
            pass
    if count == MAX_RETRIES:
        print("\tFailed to connect to ElasticSearch Database, try again you sheep !\n")


os.system(CLEAR_SYNTAXE)

# launch docker
print("\t###############\n\tStarting Docker\n\t###############\n")
os.chdir("./dockers")
dockerManager = DockerManager()
dockerManager.isDockerRunning("docker-compose up --build -d", False)
input(
    "\n\nTo continue setup, please open a different terminal and type the following commands to start to docker API :\n\n\tdocker exec -it datanode /bin/bash\n\tpython3 /app/app.py\n\n\tOnce done press a key to continue.\n\n"
)
os.chdir("../")
print("\t######################\n\tDocker Started")

# Start of ElasticSearch
print("\tStarting ElasticSearch\n\t######################\n")
startES()
print("\t#####################\n\tElasticSearch Started\n\t#####################")

input('\n\tDeployment done. Press a key and type "python app.py" to enjoy app')

# def startMongo():
#     """
#     DESC : Starts Mongo Database and tries request to be shure database is running
#     """
#     os.startfile(os.path.normpath(PATH_TO_MONGO_EXE))
#     count = 0
#     while count < MAX_RETRIES:
#         response = requests.get("http://localhost:27017/")
#         if response.status_code == 200:
#             print("\tMongoDB started !\n")
#             break
#         else:
#             print("Failed to connect to MongoDB, next attempt in 10 seconds...")
#             time.sleep(10)
#             count += 1
#     if count == MAX_RETRIES:
#         print("Failed to connect to MongoDB Database, try again you sheep !")

# # Start of MongoDB
# print("\tStarting MongoDB\n\t#####################\n")
# startMongo()
# print("\t###############\n\tMongoDB Started\n\t###############\n")
