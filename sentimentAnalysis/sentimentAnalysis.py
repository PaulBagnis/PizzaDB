from textblob import TextBlob
from re import sub, compile, UNICODE
from emoji import UNICODE_EMOJI
from nltk import wordpunct_tokenize


class SentimentAnalysis(object):
    def __init__(self):
        pass


    def calculatePolarity(self, text):
        return TextBlob(self.clean(text)).sentiment.polarity


    def calculatePolarity_baseFive(self, text):
        return float(format(5 * (( self.calculatePolarity(text)+1 )/2), '.1f'))


    def clean(self, text):
        text = sub("@[A-Za-z0-9]+","",text) #Remove @ sign
        text = sub(r"(?:\@|http?\://|https?\://|www)\S+", "", text) #Remove http links
        text = text.split()
        text = ' '.join(c for c in text if c not in UNICODE_EMOJI) #Remove Emojis
        text = text.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
        return text