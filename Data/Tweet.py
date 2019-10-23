from unidecode import unidecode
import nltk
from nltk.stem.lancaster import LancasterStemmer
from Data.TwitterConversionException import TwitterConversionException

_TAG_LIST = ['JJ', 'JJR ', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


class Tweet:

    id = None
    twitter_id = None
    created_at = None
    text = None
    filtered_text = None
    user_id = None

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

        for token in nltk.pos_tag(self.text.split()):  # Filter all words based in their types using the list _TAG_LIST
            if token[1] in _TAG_LIST:
                self.filtered_text = self.filtered_text + ' ' + st.stem(token[0])

    def get_serializable(self):
        return {"id": self.id, "twitter_id": self.twitter_id, "created_at": self.created_at, "text": self.text,
                "filtered_text": self.filter_text(), "user_id": self.user_id}