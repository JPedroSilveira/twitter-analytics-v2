from twython import TwythonStreamer
from Data.Tweet import Tweet
from Data.Hashtag import Hashtag
from Data.User import User
from Database.TableManeger import TableManeger


def save_tweet(tweet: object) -> object:
    database = TableManeger(Tweet)
    return database.save(tweet)


def save_hashtag(hashtag: object) -> object:
    database = TableManeger(Hashtag)
    return database.save(hashtag)


def save_user(user: object) -> object:
    database = TableManeger(User)
    return database.save(user)


def load_tweet(tweet_id: int) -> object:
    database = TableManeger(Tweet)
    return database.find_by_id(tweet_id)


class AnalitycalTwitterStreamer(TwythonStreamer):

    def on_success(self, data):
        tweet = Tweet()
        success = tweet.save_data(data)

        if success:
            hashtag_id_list = []
            for hashtag_data in data['entities']['hashtags']:
                hashtag = Hashtag()
                success = hashtag.save_data(hashtag_data)
                if success:
                    # hashtag = save_hashtag(hashtag)
                    hashtag_id_list.append(hashtag.id)

            user = User()
            success = user.save_data(data['user'])

            if success:
                user = save_user(user)
                tweet.save_user(user.id)
                save_tweet(tweet)

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
