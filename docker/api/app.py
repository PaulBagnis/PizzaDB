from flask import Flask
import os
import time


MAX_RETRIES = 30

app = Flask(__name__)


@app.route('/createHDFSDir')
def createHDFSDir():
    return execFunction('hdfs dfs -mkdir /FilmPosters')


@app.route('/loadToHDFS')
def loadToHDFS():
    return execFunction('hdfs dfs -copyFromLocal /home/*.jpg /FilmPosters')


def execFunction(cmd):
    nbOfTries = 0
    while str(os.system(cmd)) != 256:
        time.sleep(1)
        nbOfTries += 1
        if nbOfTries == MAX_RETRIES: return 0
    return 256


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
