from textblob import TextBlob
from re import sub
from emoji import demojize
from polyglot.detect import Detector

class SentimentAnalysis(object):
    def __init__(self):
        pass


    def calculatePolarity(self, text):
        return TextBlob(self.clean(text)).sentiment.polarity


    def calculatePolarity_baseFive(self, text):
        return float(format(5 * (( self.calculatePolarity(text)+1 )/2), '.1f'))


    def clean(self, text):
        text = sub(r'(?:\@|http?\://|https?\://|www)\S+', '', text)                 # Remove web links
        text = sub('@[A-Za-z0-9_]+','', text)                                       # Remove user links
        text = text.replace('RT : ', '').replace('RT ', '')                         # Remove RT mention
        text = text.replace('#', '').replace('\n', '.').replace('_', ' ')           # Remove useless characters
        text = sub(r'(?<!^)(?=[A-Z])', ' ', text)                                   # Convert camelcase to standart format
        try:
            language=Detector(text).language.code                                   # Find the language
        except:
            language='en'                                                           # If no language is found set it to 'english'
        text= demojize(text, language=language).replace(':', '').replace('_', ' ')  # Convert emoji to clear string
        text = ' '.join(w for w in text.split(' ') if w)                            # clear spacing
        return text

