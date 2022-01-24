from polyglot.detect import Detector
from textblob import TextBlob
from emoji import demojize
from re import sub


class SentimentAnalysis(object):
    def __init__(self):
        """ 
        DESC :
        IN   :  
        OUT  : 
        """
        self.supported_languages = ['es', 'pt', 'it', 'fr', 'de', 'en']

    def calculatePolarity(self, text):
        """ 
        DESC :
        IN   :  
        OUT  : 
        """
        return TextBlob(self.clean(text)).sentiment.polarity

    def calculatePolarity_baseFive(self, text):
        """ 
        DESC :
        IN   :  
        OUT  : 
        """
        return float(format(5 * ((self.calculatePolarity(text) + 1) / 2), '.1f'))

    def clean(self, text):
        """ 
        DESC :
        IN   :  
        OUT  : 
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
        DESC :
        IN   :  
        OUT  : 
        """
        try:
            # remove emojis
            text = sub(r':([A-Za-z0-9_]*):', '', demojize(text))
            language = Detector(text).language.code
            # Find the language
            if language in self.supported_languages:
                # Convert emoji to clear string
                return (demojize(text, language=language).replace(':', '').replace('_', ' '))
        except:
            pass
        return text
