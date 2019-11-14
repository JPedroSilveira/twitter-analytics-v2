from Data.Error.TwitterConversionException import TwitterConversionException
from Database.DBData import DBData


class User(DBData):
    twitter_id = 0
    name = ''
    name_size = 100
    followers_count = 0
    location = ''
    location_size = 100

    def save_data(self, user_data):
        try:
            location = user_data['location']
            self.twitter_id = user_data['id']
            self.name = user_data['name']
            self.followers_count = user_data['followers_count']

            if location is not None:
                self.location = location

            return True
        except KeyError:
            exception = TwitterConversionException(user_data, self)
            exception.error_handling()
            return False
