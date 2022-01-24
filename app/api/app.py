from flask import Flask
import os

app = Flask(__name__)
MAX_RETRIES = 5

@app.route('/createHDFSDir')
def createHDFSDir():
   exitCode = str(os.system("hdfs dfs -mkdir /FilmPosters"))
   return exitCode

@app.route('/loadToHDFS')
def loadToHDFS():
   exitCode = str(os.system("hdfs dfs -copyFromLocal /home/*.jpg /FilmPosters"))
   return exitCode

# shell2http.register_command(endpoint="createHDFSDir", command_name="hdfs dfs -mkdir /FilmPosters")
# shell2http.register_command(endpoint="loadToHDFS", command_name="hdfs dfs -copyFromLocal /home/*.jpg /FilmPosters")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 