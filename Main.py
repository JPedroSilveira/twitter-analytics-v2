from Twitter.TwitterCore import TwitterCore
from Database.TableManeger import TableManeger
from Data.Tweet import Tweet
# import nltk


def main():
    # nltk.download('punkt')

    twitter = TwitterCore()

    twitter.stream('Trump', 'en')

    #maneger = TableManeger(Tweet)

    #maneger.find_by_id(1)

    #maneger.delete_by_id(1)

    #maneger.find_by_id(1)


main()
