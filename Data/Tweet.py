from unidecode import unidecode
import nltk
from nltk.stem.lancaster import LancasterStemmer
from Data.Error.TwitterConversionException import TwitterConversionException
from Database.Cons import SupportedTypes

_TAG_LIST = ['JJ', 'JJR ', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


class Tweet:

    id = 0
    twitter_id = 0
    user_id = 0
    created_at = ''
    created_at_size = 50
    text = ''
    text_size = 280
    filtered_text = ''
    filtered_text_size = 280
    test = [1,-5,9,10,222,34,231,121,325535,34634,123,123213,3221]
    test_size = 13
    test_type = SupportedTypes.INT_NAME

    def save_data(self, tweet_data):
        try:
            self.twitter_id = tweet_data['id']
            self.text = unidecode(tweet_data['text'])
            self.created_at = tweet_data['created_at']
            self.filter_text()
            return True
        except KeyError:
            exception = TwitterConversionException(tweet_data, self)
            exception.error_handling()
            return False

    def save_user(self, user_id):
        self.user_id = user_id

    def filter_text(self):
        st = LancasterStemmer()  # Normalize the words
        self.filtered_text = ''  # Initialize the string

        # Filter all words based in their types using the list _TAG_LIST
        for token in nltk.pos_tag(self.text.lower().split()):
            if token[1] in _TAG_LIST:
                self.filtered_text = self.filtered_text + ' ' + st.stem(token[0])