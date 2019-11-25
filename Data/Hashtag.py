from Data.Error.TwitterConversionException import TwitterConversionException
from Database.Cons import Values
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeInt
from Database.TableManager import TableManager as DBManager
from Database.Error import ClassError as DBError
from Database.DBData import DBData


class Hashtag(DBData):
    text = Values.STRING_EMPTY
    text_size = 280

    def __init__(self):
        self.tweet_id = Values.INT_EMPTY

    def set(self, hashtag_data, tweet):
        try:
            if DBManager.is_saved(tweet):
                self.text = hashtag_data['text']
                self.tweet_id = tweet.id
                return True
            else:
                raise DBError.ChildNotFoundInDataBase("You need to save Tweet and Hashtag before set a TweetHashtag entity!")
        except KeyError:
            exception = TwitterConversionException(hashtag_data, self)
            exception.error_handling()
            return False

    def db_save(self):
        if self.id != Values.INT_EMPTY:
            dbm = DBManager(Hashtag)
            dbm.save(self)
            bt_hashtag = BTree('hashtag_tweet', BTreeNodeInt, Hashtag)
            bt_hashtag.insert(self.id, self.tweet_id)
        else:
            raise cs.ChildNotFoundInDataBase("You need to set Tweet and Hashtag before saving!")

    def db_delete(self):
        if DBManager.is_saved(self):
            dbm = DBManager(Hashtag)
            dbm.delete(self)

    def get_tweets(self) -> list:
        if DBManager.is_saved(self):
            bt_hashtag = BTree('hashtag_tweet', BTreeNodeInt, Hashtag)
            return bt_hashtag.find(self.id)
        else:
            return []

