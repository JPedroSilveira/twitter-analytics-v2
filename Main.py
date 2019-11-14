from Data.Tweet import Tweet
from Database.TableManager import TableManager
from Twitter.TwitterCore import TwitterCore
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeInt


def load_twitter_stream_to_save():
    twitter = TwitterCore()

    twitter.stream('Trump', 'en')


def find_update_delete_test():
    manager = TableManager(Tweet)

    obj_1 = manager.find_by_id(0)

    obj_2 = manager.find_by_id(1)

    obj_3 = manager.find_by_id(2)

    obj_3.text = 'oi'
    obj_3.test = ['oi', 'tchau']

    manager.save(obj_3)

    manager.delete_by_id(1)

    obj_1 = manager.find_by_id(0)

    obj_2 = manager.find_by_id(1)

    obj_3 = manager.find_by_id(2)

    obj_3 = manager.find_by_id(2)


def main():
    # nltk.download('punkt')

    #find_update_delete_test()
    #load_twitter_stream_to_save()

    teste = BTree('tweet_id', BTreeNodeInt, Tweet)

    teste2 = BTree('tweet_id', BTreeNodeInt, Tweet)

    teste3 = BTree('tweet_id', BTreeNodeInt, Tweet)

main()
