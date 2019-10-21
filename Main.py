from Twitter.TwitterCore import TwitterCore
import nltk


def main():
    nltk.download('punkt')

    twitter = TwitterCore()

    twitter.stream('Trump', 'en')


main()
