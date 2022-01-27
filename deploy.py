from tools.elasticSearch import ElasticSearchClient
from dockers.app import DockerManager

from sys import platform
import os

CLEAR_SYNTAXE = 'cls' if platform == 'win32' else 'clear'


def deploy():
    elasticSearchClient = ElasticSearchClient()
    elasticSearchClient.start()

    # Starts Docker
    os.chdir("./dockers")
    dockerManager = DockerManager()
    os.chdir("../")
    dockerManager.start(True)
    
    os.system(CLEAR_SYNTAXE)
    input("\n\n \
            To continue setup, please open a different terminal and \
            type the following commands to start to docker API :\n\n \
                \tdocker exec -it datanode /bin/bash\n \
                \tpython3 /app/app.py\n \
            \n\nOnce done press enter to continue.\n\n"
    )
    os.system(CLEAR_SYNTAXE)
    input('\n\t \
            Deployment done. Press a enter and type: \
            "python app.py" \
            \n\nEnjoy the app')


if __name__ == '__main__':
    deploy()