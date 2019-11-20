from twython import TwythonStreamer

from Data.Hashtag import Hashtag
from Data.Tweet import Tweet
from Data.User import User
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeInt, BTreeNode280String
from Database.TableManager import TableManager


def save_tweet(tweet: object) -> object:
    database = TableManager(Tweet)

    return database.save(tweet)


def save_hashtag(hashtag: object, tweet: object) -> object:
    database = TableManager(Hashtag)
    bt_hashtag_text = BTree('hashtag_text', BTreeNode280String, Hashtag)
    id = bt_hashtag_text.find(hashtag.text)

    if id is None:
        database.save(hashtag)
        bt_hashtag_text.insert(hashtag.text, hashtag.id)

    bt_hashtag_tweet = BTree('hashtag_tweet_'+hashtag.text, BTreeNodeInt, Hashtag)
    bt_hashtag_tweet.insert(tweet.id, tweet.id)


def save_user(user: object) -> object:
    database = TableManager(User)
    bt_twitter_id = BTree('twitter_id', BTreeNodeInt, User)
    id = bt_twitter_id.find(user.twitter_id)

    # Insert
    if id is None:
        database.save(User)
        bt_twitter_id.insert(user.twitter_id, user.id)
    else:  # Update
        user.id = id
        database.save(User)


def load_tweet(tweet_id: int) -> object:
    database = TableManager(Tweet)
    return database.find_by_id(tweet_id)


class AnalitycalTwitterStreamer(TwythonStreamer):

    def on_success(self, data):
        tweet = Tweet()
        success = tweet.save_data(data)

        if success:
            user = User()
            success = user.save_data(data['user'])

            if success:
                save_user(user)
                tweet.save_user(user.id)
                save_tweet(tweet)

                for hashtag_data in data['entities']['hashtags']:
                    hashtag = Hashtag()
                    success = hashtag.save_data(hashtag_data)
                    if success:
                        save_hashtag(hashtag, tweet)

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
