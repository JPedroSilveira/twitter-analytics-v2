from Core import NaturalLanguage
from Data.Error.TwitterConversionException import TwitterConversionException
from Database.Error import ClassError as DBError
from Database.Cons import Values
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeInt, BTreeNode280String
from Database.TableManager import TableManager as DBManager
from Database.DBData import DBData


class User(DBData):
    twitter_id = Values.INT_EMPTY
    name = Values.STRING_EMPTY
    name_size = 100
    followers_count = Values.INT_EMPTY
    location = Values.STRING_EMPTY
    location_size = 100

    def find_self(self):
        bt_twitter_id_user = BTree('twitter_id_user', BTreeNodeInt, User, User)
        saved_self = bt_twitter_id_user.find_first_or_default(self.twitter_id)

        if saved_self is not None:
            self.id = saved_self.id
            self.saved = saved_self.saved

        return saved_self

    def set(self, user_data):
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

    def db_save(self):
        dbm = DBManager(User)
        dbm.save(self)

        if not DBManager.is_saved(self):
            bt_twitter_id_user = BTree('twitter_id_user', BTreeNodeInt, User, User)
            bt_twitter_id_user.insert(self.twitter_id, self.id)

    def load(id):
        dbm = DBManager(User)
        return dbm.find_by_id(id)

    def get_tweets(self):
        if DBManager.is_saved(self):
            bt_user_tweet = BTree('user_tweet', BTreeNodeInt, User, Tweet)
            return bt_user_tweet.find(self.id)


class Tweet(DBData):
    tweet_id = Values.INT_EMPTY
    user_id = Values.INT_EMPTY
    created_at = Values.STRING_EMPTY
    created_at_size = 50
    text = Values.STRING_EMPTY
    text_size = 280
    filtered_text = Values.STRING_EMPTY
    filtered_text_size = 280

    def __init__(self):
        self.hashtag_ids = Values.LIST_EMPTY()

    def find_self(self):
        tweet_id_tweet = BTree('tweet_id_tweet', BTreeNodeInt, Tweet, Tweet)
        saved_self = tweet_id_tweet.find_first_or_default(self.tweet_id)

        if saved_self is not None:
            self.id = saved_self.id
            self.saved = saved_self.saved

        return saved_self

    def set(self, tweet_data):
        try:
            self.tweet_id = tweet_data['id']
            self.text = tweet_data['text']
            self.created_at = tweet_data['created_at']
            self.filtered_text = NaturalLanguage.filter_text(self.text)

            return True
        except KeyError:
            exception = TwitterConversionException(tweet_data, self)
            exception.error_handling()
            return False

    def set_user(self, user):
        self.user_id = user.id

    def set_hashtags(self, hashtags):
        for hashtag in hashtags:
            if DBManager.is_saved(hashtag):
                self.hashtag_ids.append(hashtag.id)

    def db_save(self):
        if self.user_id != Values.INT_EMPTY:
            if not DBManager.is_saved(self):
                dbm = DBManager(Tweet)
                dbm.save(self)

                tweet_id_tweet = BTree('tweet_id_tweet', BTreeNodeInt, Tweet, Tweet)
                tweet_id_tweet.insert(self.tweet_id, self.id)

                for hashtag_id in self.hashtag_ids:
                    bt_tweet_hashtag = BTree('tweet_hashtag', BTreeNodeInt, Tweet, Hashtag)
                    bt_tweet_hashtag.insert(self.id, hashtag_id)

                bt_user_tweet = BTree('user_tweet', BTreeNodeInt, User, Tweet)
                bt_user_tweet.insert(self.user_id, self.id)
        else:
            raise DBError.ChildNotFoundInDataBase("You need to set User before saving a Tweet!")

    def load(id):
        dbm = DBManager(Tweet)
        return dbm.find_by_id(id)

    def db_delete(self):
        if DBManager.is_saved(self):
            dbm = DBManager(Tweet)
            dbm.delete(self)

    def get_user(self) -> object:
        if self.user_id != Values.INT_EMPTY:
            dbm = DBManager(User)
            return dbm.find_by_id(self.user_id)
        else:
            return []

    def get_hashtags(self) -> list:
        if DBManager.is_saved(self):
            bt_tweet_hashtag = BTree('tweet_hashtag', BTreeNodeInt, Tweet, Hashtag)
            return bt_tweet_hashtag.find(self.id)


class Hashtag(DBData):
    text = Values.STRING_EMPTY
    text_size = 280

    def find_self(self):
        hashtag_text_hashtag = BTree('hashtag_text_hashtag', BTreeNode280String, Hashtag, Hashtag)
        saved_self = hashtag_text_hashtag.find_first_or_default(self.text)

        if saved_self is not None:
            self.id = saved_self.id
            self.saved = saved_self.saved

        return saved_self

    def set(self, hashtag_data):
        try:
            self.text = hashtag_data['text']
            return True
        except KeyError:
            exception = TwitterConversionException(hashtag_data, self)
            exception.error_handling()
            return False

    def db_save(self):
        dbm = DBManager(Hashtag)
        dbm.save(self)
        hashtag_text_hashtag = BTree('hashtag_text_hashtag', BTreeNode280String, Hashtag, Hashtag)
        hashtag_text_hashtag.insert(self.text, self.id)

    def load(id):
        dbm = DBManager(Hashtag)
        return dbm.find_by_id(id)

    def add_tweet(self, tweet):
        bt_hashtag_tweet = BTree('hashtag_tweet', BTreeNodeInt, Hashtag, Tweet)
        bt_hashtag_tweet.insert(self.id, tweet.id)

    def db_delete(self):
        if DBManager.is_saved(self):
            dbm = DBManager(Hashtag)
            dbm.delete(self)

    def get_tweets(self) -> list:
        if DBManager.is_saved(self):
            bt_hashtag = BTree('hashtag_tweet', BTreeNodeInt, Hashtag, Tweet)
            return bt_hashtag.find(self.id)
        else:
            return []