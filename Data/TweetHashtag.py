from Data.Error.TwitterConversionException import TwitterConversionException
from Database.Cons import Values
from Database.DBData import DBData
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeInt
from Database.TableManager import TableManager as db, TableManager
from Database.Error import ClassError as DBError


class TweetHashtag(DBData):
    id_tweet = Values.INT_EMPTY
    id_hashtag = Values.INT_EMPTY

    def set(self, tweet, hashtag, text_pos):
        if db.is_saved(tweet) and db.is_saved(hashtag):
            self.id_tweet = tweet.id
            self.id_hashtag = hashtag.id
            self.text_pos = text_pos
        else:
            raise DBError.ChildNotFoundInDataBase("You need to save Tweet and Hashtag before set a TweetHashtag entity!")

    def db_save(self):
        if self.id_tweet != Values.INT_EMPTY and self.id_hashtag != Values.INT_EMPTYs:
            TableManager(TweetHashtag)
            bt_tweet = BTree('tweethashtag_tweet', BTreeNodeInt, TweetHashtag)
            bt_tweet.insert(self.id_tweet, self.id_hashtag)
            bt_hashtag = BTree('tweethashtag_hashtag', BTreeNodeInt, TweetHashtag)
            bt_hashtag.insert(self.id_hashtag, self.id_tweet)
        else:
            raise cs.ChildNotFoundInDataBase("You need to set Tweet and Hashtag before saving!")

    def db_delete(self):
        if db.is_saved(self):
            db_th = TableManager(TweetHashtag)
            db_th.delete(self)

    def get_all_hashtags(self) -> list:
        if self.id_tweet != Values.INT_EMPTY:
            bt_tweet = BTree('tweethashtag_tweet', BTreeNodeInt, TweetHashtag)
            return bt_tweet.find(self.id_tweet)
        else:
            return []

    def get_all_tweets(self) -> list:
        if self.id_hashtag != Values.FLOAT_EMPTY

