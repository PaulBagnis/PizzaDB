import tmdbsimple as tmdb
import requests
import os
import re
from alphabet_detector import AlphabetDetector
from sys import platform


CLEAR_SYNTAXE = 'cls' if platform == 'win32' else 'clear'


class TMDbClient(object):
    def __init__(self, img_dir_path=os.path.join(os.getcwd(), 'images')):
        """
        DESC : set up tmdb API and fetch actu

        IN   : img_dir_path -  define the image dir ( default is eq to <mainApp>/images ) 
        """
        tmdb.API_KEY = '678b941591dc9bdb6ec1352563253fdd'
        tmdb.REQUESTS_TIMEOUT = 10
        tmdb.REQUESTS_SESSION = requests.Session()
        
        self.img_dir_path = img_dir_path

    def movieMenu(self):
        """
        DESC : Display a list of recent movies to choose from

        OUT  : the ID and title of the choosen movie
        """
        movie_list = [movie for movie in tmdb.Movies().now_playing()['results'] 
                        if AlphabetDetector().only_alphabet_chars(movie['original_title'], 'LATIN')]
        warning=''
        while True:
            # os.system(CLEAR_SYNTAXE)
            print('\n\nList of available movies :\n')
            for p, movie in enumerate(movie_list):
                print('{} : {}'.format(p, movie['original_title']))
            choice = input('\nWhat movie do you want info on ?\n{} > '.format(warning))
            # Test if choice is an Integer in the range of the menu
            if choice.isnumeric():
                choice=int(choice)
                if 0 <= choice <= p:
                    return movie_list[choice]['id'], re.sub(r'[^\w\-\. ]', '_', movie_list[choice]['original_title'])
                else:
                    warning='An existing one this time...\n'
            else:
                warning='A number will work great too...\n'

    def downloadPic(self, movie_id):
        """
        DESC : Download a movie poster based on his ID

        IN   : movie_id - id of the movie that we'll download
        OUT  : file path
        """
        # Test if directory exists in working directory, if not, creates it
        if not os.path.isdir(self.img_dir_path):
            try:
                os.mkdir(self.img_dir_path)
                print('../images directory created')
            except Exception as e:
                print('Error :' + e +
                'Failed to create ../images directory, please launch in administrator privileges')
        
        url = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'+ \
                    tmdb.Movies(movie_id).info()['poster_path']
        img_path='{}/{}.{}'.format(self.img_dir_path, movie_id, url.split('.')[-1])
        # Test if file already exists if not, download it
        if not os.path.exists(img_path):
            response = requests.get(url, stream=True)
            if not response.ok:
                print('Failed to get image from Movie. Please try again ¯\_(ツ)_/¯')
                return 0
            with open(img_path, 'wb') as file:
                for block in response.iter_content(1024):
                    if not block: break
                    file.write(block)
            return img_path
        return img_path

    def deletePicDir(self):
        """
        DESC : Delete the directory used to store downloaded pictures

        OUT  : 0|1 success or not
        """
        if os.path.isdir(self.img_dir_path):
            for pic in os.listdir(self.img_dir_path):
                os.remove('{}/{}'.format(self.img_dir_path, pic))
            return os.rmdir(self.img_dir_path)
        else:
            return 0

