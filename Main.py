from Data.Tweet import Tweet
from Twitter.TwitterCore import TwitterCore


def start_twitter_stream():
    twitter = TwitterCore()

    twitter.stream('Trump', 'en')


def readCSV():
    tweets = []

    with open('.\\Dataset\\train.csv', encoding='utf8') as dataset:
        lines = dataset.readlines()

        for line in range(1, len(lines)):
            data = lines[line].split(',', 2)
            tweet = Tweet()
            tweet.tweet_id = int(data[0])
            tweet.negative = data[1] == '1'
            tweet.text = data[2]

            tweets = tweets[:] + [tweet]

    print('All tweets loaded')


def main():
    # nltk.download('punkt')

    # start_twitter_stream()

    readCSV()


main()
