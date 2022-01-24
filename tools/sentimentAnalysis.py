from polyglot.detect import Detector
from textblob import TextBlob
from emoji import demojize
from re import sub


class SentimentAnalysis(object):
    def __init__(self):
        """ 
        DESC : init supported_languages that store languages handled by the emoji librairy  
        """
        self.supported_languages = ['es', 'pt', 'it', 'fr', 'de', 'en']

    def calculatePolarity(self, text):
        """ 
        DESC : analyse the posivity of a text

        IN   : text - text that will be used
        OUT  : a float between -1 & 1 (from bad to good)
        """
        return TextBlob(self.clean(text)).sentiment.polarity

    def calculatePolarity_baseFive(self, text):
        """ 
        DESC : convert the -1 to 1 rating of positivy to a clearer 0 to 5 rating (with 2 number precision) 
        
        IN   : text - text that will be used
        OUT  : a float between 0 & 5 (from bad to good)
        """
        return float(format(5 * ((self.calculatePolarity(text) + 1) / 2), '.1f'))

    def clean(self, text):
        """ 
        DESC : clean the text to improve the sentiment analysis precision

        IN   : text - text that will be convert
        OUT  : a raw text without crapy internet stuffs
        """
        # Remove web links
        text = sub(r'(?:\@|http?\://|https?\://|www)\S+', '', text)
        # Remove user links
        text = sub('@[A-Za-z0-9_]+', '', text)
        # Remove RT mention  
        text = text.replace('RT : ', '').replace('RT ', '')
        # Remove useless characters
        text = (text.replace('#', '').replace('\n', '.').replace('_', ' '))
        # Convert camelcase to standart format
        text = sub(r'(?<!^)(?=[A-Z])', ' ', text)
        text = self.handleEmoji(text)
        # clear spacing
        text = ' '.join(w for w in text.split(' ') if w)
        return text

    def handleEmoji(self, text):
        """ 
        DESC : emoji are not yet supported by the sentiment analysis librairy so we have to handle them. If the language is supported we convert them into plain understandable text, else they're deleted 

        IN   : text - text that will be convert
        OUT  : text without emojis

        """
        try:
            # remove emojis
            text = sub(r':([A-Za-z0-9_]*):', '', demojize(text))
            # use the text without emoji to figure the language 
            language = Detector(text).language.code
            # check if the language is supported
            if language in self.supported_languages:
                # Convert emoji to plain text
                return (demojize(text, language=language).replace(':', '').replace('_', ' '))
        except:
            pass
        return text
