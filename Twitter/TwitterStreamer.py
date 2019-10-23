from twython import TwythonStreamer
from Data.Tweet import Tweet
from Data.Hashtag import Hashtag
from Data.User import User
from Database.Maneger import Maneger


def save_tweet(tweet):
    database = Maneger(Tweet)
    database.save(tweet)


def load_tweet(tweet_id):
    database = Maneger(Tweet)
    return database.find_by_id(tweet_id)


class AnalitycalTwitterStreamer(TwythonStreamer):

    def on_success(self, data):
        tweet = Tweet()
        success = tweet.save_data(data)

        if success:
            hashtag_list = []
            for hashtag_data in data['entities']['hashtags']:
                hashtag = Hashtag()
                success = hashtag.save_data(hashtag_data)
                if success:
                    hashtag_list.append(hashtag)

            user = User()
            success = user.save_data(data['user'])

            if success:
                tweet.save_user(user.id)

                save_tweet(tweet)

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
