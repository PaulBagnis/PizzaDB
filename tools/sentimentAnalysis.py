from polyglot.detect import Detector
from textblob import TextBlob
from emoji import demojize
from re import sub


class SentimentAnalysis(object):
    def __init__(self):
        self.supported_languages = ['es', 'pt', 'it', 'fr', 'de', 'en']

    def calculatePolarity(self, text):
        return TextBlob(self.clean(text)).sentiment.polarity

    def calculatePolarity_baseFive(self, text):
        return float(format(5 * ((self.calculatePolarity(text) + 1) / 2), '.1f'))

    def clean(self, text):
        text = sub(r'(?:\@|http?\://|https?\://|www)\S+', '', text)  # Remove web links
        text = sub('@[A-Za-z0-9_]+', '', text)  # Remove user links
        text = text.replace('RT : ', '').replace('RT ', '')  # Remove RT mention
        text = (text.replace('#', '').replace('\n', '.').replace('_', ' '))  # Remove useless characters
        text = sub(r'(?<!^)(?=[A-Z])', ' ', text)  # Convert camelcase to standart format
        text = self.handleEmoji(text)
        text = ' '.join(w for w in text.split(' ') if w)  # clear spacing
        return text

    def handleEmoji(self, text):
        try:
            text = sub(r':([A-Za-z0-9_]*):', '', demojize(text))  # remove emojis
            language = Detector(text).language.code  # Find the language
            if language in self.supported_languages:
                return (demojize(text, language=language).replace(':', '').replace('_', ' '))  # Convert emoji to clear string
        except:
            pass
        return text
