from twython import Twython

from Twitter.TwitterCredentials import Credentials
from Twitter.TwitterStreamer import AnalitycalTwitterStreamer


class TwitterCore:

    def __init__(self):
        credentials = Credentials()
        self.twitter_access = Twython(credentials.consumer_key, credentials.consumer_secret)
        self.twitter_stream = AnalitycalTwitterStreamer(credentials.consumer_key, credentials.consumer_secret,
                                                        credentials.access_token, credentials.access_secret)

    def query_popular_by_text(self, text: str, count: int) -> list:
        query = {'q': text,
                 'result_type': 'popular',
                 'count': count,
                 'lang': 'en',
                 }

        dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}

        for status in self.twitter_access.search(**query)['statuses']:
            dict_['user'].append(status['user']['screen_name'])
            dict_['date'].append(status['created_at'])
            dict_['text'].append(status['text'])
            dict_['favorite_count'].append(status['favorite_count'])

        return dict_

    def stream(self, tweet_track, tweet_language):
        self.twitter_stream.statuses.filter(track=tweet_track, language=tweet_language)
