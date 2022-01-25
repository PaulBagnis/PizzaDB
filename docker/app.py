import requests
import docker
import time
import os


class DockerManager(object):
    def __init__(self, api_url='http://localhost:5000/'):
        """
        DESC : create a docker client from the dockerfile locate on the same directory level

        IN   : api_url - base url for docker small custom flask api 
        """
        self.docker_client = docker.from_env()
        self.api_docker_base_url = api_url

    def isContainerRunning(self, container_name):
        """
        DESC : check if container is running

        IN   : container_name - the name of the container
        OUT  : return True if it's running, else False
        """
        try:
            return self.docker_client.inspect_container(container_name)['State']['Status'] == 'running'
        except Exception as e:
            print('Error :' + e)
            return False

    def isDockerRunning(self, dockerComposeCommand='docker-compose up -d', restart=False):
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
                if self.isContainerRunning('datanode'):
                    break
            except:
                print(self.isContainerRunning('datanode') + '\n\n\tPlease run docker before lauching program\n\n')
                quit()
            time.sleep(5)

    def reqToDocker(self, endpoint):

        """
        DESC : send request to the docker API

        IN   : url - endpoint
        """
        if requests.get(self.api_docker_base_url + endpoint) == '256': 
            print('\tZEPARTIIII')
        else:
            print('\tSomething went wrong ¯\_(ツ)_/¯')



