from Data.Tweet import Tweet
from Data.User import User
from Database.TableManager import TableManager
from Twitter.TwitterCore import TwitterCore
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeFloat


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

    teste0 = BTree('tweet_id', BTreeNodeFloat, Tweet)

    manager = TableManager(User)

    manager = TableManager(Tweet)

    manager.drop()

    return

    manager = TableManager(Tweet)

    manager.drop()

    return

    teste = BTree('tweet_id', BTreeNodeFloat, Tweet)

    teste.insert(10, 10)
    teste.insert(20, 20)

    #Split root
    teste.insert(30, 30)

    teste2 = BTree('tweet_id', BTreeNodeFloat, Tweet)

    teste2.insert(40, 40)
    teste2.insert(15, 15)

    #Split non root
    teste2.insert(25, 25)

    teste3 = BTree('tweet_id', BTreeNodeFloat, Tweet)

    # Double Split, one at root
    teste3.insert(5, 5)

    teste4 = BTree('tweet_id', BTreeNodeFloat, Tweet)

    teste4.insert(24, 24)

    # Split leaf
    teste4.insert(23, 23)

    teste4.insert(22, 22)

    #Split leaf and parent_node, increase root
    teste4.insert(21, 21)

    teste4.insert(6, 6)

    # Split leaf
    teste4.insert(7, 7)

    teste4.insert(4, 4)

    # Split leaf, parent_node and root
    teste4.insert(3, 3)

    teste5 = BTree('tweet_id', BTreeNodeFloat, Tweet)

main()
