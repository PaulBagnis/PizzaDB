from flask import Flask
import os
import time

app = Flask(__name__)
MAX_RETRIES = 30


@app.route("/createHDFSDir")
def createHDFSDir():
    nbOfTries = 0
    while str(os.system("hdfs dfs -mkdir /FilmPosters")) != "256":
        if nbOfTries == MAX_RETRIES:
            return "0"
        time.sleep(1)
        nbOfTries += 1
    return "256"


@app.route("/loadToHDFS")
def loadToHDFS():
    nbOfTries = 0
    while str(os.system("hdfs dfs -copyFromLocal /home/*.jpg /FilmPosters")) != "256":
        if nbOfTries == MAX_RETRIES:
            return "0"
        time.sleep(1)
        nbOfTries += 1
    return "256"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
