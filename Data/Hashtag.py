from Data.TwitterConversionException import TwitterConversionException


class Hashtag:

    def __init__(self):
        self.text = None
        self.id = None
        self.tweet_list = []

    def save_data(self, hashtag_data):
        try:
            self.text = hashtag_data['text']
            return True
        except KeyError:
            exception = TwitterConversionException(hashtag_data, self)
            exception.error_handling()
            return False
