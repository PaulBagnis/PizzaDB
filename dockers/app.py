from pywebhdfs.webhdfs import PyWebHdfsClient
from sys import platform
import requests
import docker
from time import sleep
import os


class DockerManager(object):
    def __init__(self, api_url='http://localhost:5000', host='localhost', port='9870'):
        """
        DESC : create a docker client from the dockerfile locate on the same directory level

        IN   : api_url - base url for docker small custom flask api 
        """
        self.docker_client = docker.from_env()
        self.api_docker_base_url = api_url
        self.hdfs = PyWebHdfsClient(host=host,port=port, user_name=None)

    def isContainerRunning(self, container_name):
        """
        DESC : check if container is running

        IN   : container_name - the name of the container
        OUT  : return True if it's running, else False
        """
        try:
            return self.docker_client.inspect_container(container_name)['State']['Status'] == 'running'
        except docker.errors.APIError:
            return False

    def start(self, rebuild=False, path_docker_compose='./'):
        """
        DESC : Check if docker and Hadoop image are running

        IN   : rebuild - rebuild docker containers (default: false)
               path - path to docker-compose (default: ./)
        OUT  : return True if it's running, else False
        """
        print("Docker Starting...")
        rebuild = '--build' if rebuild else ''
        sudo = 'sudo' if platform == 'linux' else ''
        starting = False
        while True:
            if not starting:
                os.chdir(path_docker_compose)
                os.popen('{} docker-compose up {} -d'.format(sudo, rebuild)).read()
                rebuild == False
                starting == True
            if self.isContainerRunning('datanode'):
                break
            else:
                print("\tFailed to connect to Docker, next attempt in 5 seconds...\n")
                sleep(5)
        print("Docker Started !")


    def createHDFSDirectory(self):
        """
        DESC : send request to create directory in HDFS
        """
        try :
            self.hdfs.make_dir('/FilmPosters')
            print('HDFS directory created !')
        except requests.exceptions.ConnectionError :
            print('Impossible to create HDFS Directory')


    def deleteHDFSDirectory(self):
        """
        DESC : send request to delete directory in HDFS
        """
        try :
            requests.delete("http://localhost:9870/webhdfs/v1/FilmPosters?op=DELETE&recursive=true")
            print('HDFS directory deleted !')
        except requests.exceptions.ConnectionError :
            print('Deletion of HDFS directory failed.')


    def reqToDocker(self, endpoint):
        """
        DESC : send request to the docker API

        IN   : url - endpoint
        """
        try:
            if requests.get('{}/{}'.format(self.api_docker_base_url, endpoint)): 
                return True
            else:
                return False
        except requests.exceptions.ConnectionError:
            print('Request failed, is your server running ?')
        
    def picToHDFS(self, pic_path):
        if self.reqToDocker('loadToHDFS'):
            print('Pic send to the HDFS folder !')
            return os.remove(pic_path)
        else:
            print('upload failed')
            return 0

