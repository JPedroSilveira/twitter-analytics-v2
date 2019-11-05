from Data.Error.TwitterConversionException import TwitterConversionException


class Hashtag:

    id = 0
    text = ''
    text_size = 100

    def save_data(self, hashtag_data):
        try:
            self.text = hashtag_data['text']
            return True
        except KeyError:
            exception = TwitterConversionException(hashtag_data, self)
            exception.error_handling()
            return False
