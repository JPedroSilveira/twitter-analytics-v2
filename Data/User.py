from Data.TwitterConversionException import TwitterConversionException


class User:
    def __init__(self):
        self.id = None
        self.twitter_id = None
        self.name = None
        self.followers_count = None
        self.location = None

    def save_data(self, user_data):
        try:
            self.twitter_id = user_data['id']
            self.name = user_data['name']
            self.followers_count = user_data['followers_count']
            self.location = user_data['location']
            return True
        except KeyError:
            exception = TwitterConversionException(user_data, self)
            exception.error_handling()
            return False
