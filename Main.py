from Twitter.TwitterCore import TwitterCore


def start_twitter_stream():
    twitter = TwitterCore()

    twitter.stream('Trump', 'en')


def main():
    # nltk.download('punkt')

    start_twitter_stream()


main()
