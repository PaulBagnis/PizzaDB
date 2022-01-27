from flask import Flask
import json
import os
import time


MAX_RETRIES = 30

app = Flask(__name__)


@app.route('/loadToHDFS')
def loadToHDFS():
    return execFunction('hdfs dfs -put /home/*.jpg /FilmPosters/ | grep \'File exists\|sasl.SaslDataTransferClient\'')


def execFunction(cmd):
    nbOfTries = 0
    while not os.system(cmd):
        time.sleep(1)
        nbOfTries += 1
        if nbOfTries == MAX_RETRIES:
            return json.dumps(False)
    return json.dumps(True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
