from flask import Flask
import os
import time

app = Flask(__name__)
MAX_RETRIES = 30


def executeCommand(command: str):
    nbOfTries = 0
    while str(os.system(command)) != "256":
        if nbOfTries == MAX_RETRIES:
            return "0"
        time.sleep(1)
        nbOfTries += 1
    return "256"


@app.route("/createHDFSDir")
def createHDFSDir():
    return executeCommand(
        "hdfs dfs -mkdir /FilmPosters"
        )


@app.route("/loadToHDFS")
def loadToHDFS():
    return executeCommand(
        "hdfs dfs -copyFromLocal /home/*.jpg /FilmPosters"
        )


@app.route("/pullFromHDFS/<int:id>")
def pullFromHDFS(id):
    return executeCommand(
        "hdfs dfs -copyToLocal /FilmPosters/" + str(id) + ".jpg /home"
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
