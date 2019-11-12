from Data.Tweet import Tweet
from Database.TableManeger import TableManeger
from Twitter.TwitterCore import TwitterCore


# import nltk


def main():
    print('oi')
    # nltk.download('punkt')

    #load_twitter_stream_to_save()

    #save_find_delete_test()


main()


def load_twitter_stream_to_save():
    twitter = TwitterCore()

    twitter.stream('Trump', 'en')


def save_find_delete_test():
    maneger = TableManeger(Tweet)

    obj_1 = maneger.find_by_id(0)

    obj_2 = maneger.find_by_id(1)

    obj_3 = maneger.find_by_id(2)

    maneger.delete_by_id(1)

    obj_1 = maneger.find_by_id(0)

    obj_2 = maneger.find_by_id(1)

    obj_3 = maneger.find_by_id(2)

    obj_3 = maneger.find_by_id(2)

    return