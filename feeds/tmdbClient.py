import tmdbsimple as tmdb
import requests
import os
from alphabet_detector import AlphabetDetector
from sys import platform


CLEAR_SYNTAXE = 'cls' if platform == 'win32' else 'clear'


class RSSClient(object):
    def __init__(self, img_path=os.path.join(os.getcwd(), 'images')):
        """
        DESC : set up tmdb API and fetch actu

        IN   : img_path -  define the image dir ( default is eq to <mainApp>/images ) 
        """
        tmdb.API_KEY = '678b941591dc9bdb6ec1352563253fdd'
        tmdb.REQUESTS_TIMEOUT = 10
        tmdb.REQUESTS_SESSION = requests.Session()
        
        self.tmdb_movies = tmdb.Movies()
        self.img_path = img_path

    def movieMenu(self, now_playing):
        """
        DESC : Display a list of movies to choose from

        IN   : now_playing - list of recent movies
        OUT  : the position of the choosen movie
        """
        warning=''
        while True:
            os.system(CLEAR_SYNTAXE)
            print('\n\nList of available movies :\n')
            for p, movie in enumerate(now_playing):
                if AlphabetDetector().only_alphabet_chars(movie['original_title'], 'LATIN'):
                    print('{} : {}'.format(p, movie['original_title']))

            choice = input('\nWhat movie do you want info on ?\n{} > '.format(warning))

            # Test if choice is an Integer in the range of the menu
            if choice.isnumeric():
                if 0 <= int(choice) <= p:
                    return int(choice)
                else:
                    warning='An existing one this time...\n'
            else:
                warning='A number will work great too...\n'

    def downloadPic(self, movie_id):
        """
        DESC : Download a movie poster

        IN   : movie_id - id of the movie that we'll download
        OUT  : 0|1 success or not
        """
        # Test if directory exists in working directory, if not, creates it
        if not os.path.isdir(self.img_path):
            try:
                os.mkdir(self.img_path)
                print('../images directory created')
            except Exception as e:
                print('Error :' + e +
                'Failed to create ../images directory, please launch in administrator privileges')
        # Test if file already exists if not, download it
        if not os.path.exists(self.img_path):
            url = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'+ \
                    tmdb.Movies(movie_id).info()['poster_path']
            response = requests.get(url, stream=True)
            if not response.ok:
                print('Failed to get image from Movie. Please try again ¯\_(ツ)_/¯')
                return 0
            with open('{}/{}.{}'.format(self.img_path, movie_id, url.split('.')[-1]), 'wb') as file:
                for block in response.iter_content(1024):
                    if not block: break
                    file.write(block)
            return 1
    
    def chooseMovieToDownload(self):
        """
        DESC : choose a movie to download based on recent release
        OUT  : 0|1 success or not 
        """
        movies=self.tmdb_movies.now_playing()['results']
        return self.downloadPic(movies[self.movieMenu(movies)]['id'])

    def RefreshMovies(self):
        """
        DESC : Fetch the last releases
        """
        self.tmdb_movies = tmdb.Movies()
        return self.tmdb_movies