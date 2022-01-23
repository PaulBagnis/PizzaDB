from textblob import TextBlob
from re import sub

class SentimentAnalysis(object):
    def __init__(self):
        pass

    def calculatePolarity(self, text):
        return TextBlob(self.clean(text)).sentiment.polarity


    def calculatePolarity_baseFive(self, text):
        return float(format(5 * (( self.calculatePolarity(text)+1 )/2), '.1f'))


    def clean(self, text):
        return ' '.join(sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', text).split())