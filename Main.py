import nltk
from Data.Tweet import Tweet
from Database.TableManager import TableManager
from Twitter.TwitterCore import TwitterCore


def load_twitter_stream_to_save():
    twitter = TwitterCore()

    twitter.stream('Trump', 'en')


def save_find_update_delete_test():
    manager = TableManager(Tweet)

    obj_1 = manager.find_by_id(0)

    obj_2 = manager.find_by_id(1)

    obj_3 = manager.find_by_id(2)

    obj_3.text = 'oi'
    obj_3.test = ['oi', 'tchau']

    manager.update(obj_3)

    manager.delete_by_id(1)

    obj_1 = manager.find_by_id(0)

    obj_2 = manager.find_by_id(1)

    obj_3 = manager.find_by_id(2)

    obj_3 = manager.find_by_id(2)


def main():
    print('oi')
    # nltk.download('punkt')

    # load_twitter_stream_to_save()

    # save_find_update_delete_test()


main()
