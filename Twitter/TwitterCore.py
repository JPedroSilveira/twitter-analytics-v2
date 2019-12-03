from requests.exceptions import ChunkedEncodingError
from twython import Twython

from Database.DBData import DBData
from Database.DBManager import DBManager
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNode50String
from Twitter.TwitterCredentials import Credentials
from Twitter.TwitterStreamer import AnalitycalTwitterStreamer


class TwitterCore(DBData):

    data_name = ''
    data_name_size = 50
    tweets = 0
    negative_count = 0
    positive_count = 0

    def __init__(self):
        credentials = Credentials()
        self.twitter_access = Twython(credentials.consumer_key, credentials.consumer_secret)
        self.twitter_stream = AnalitycalTwitterStreamer(credentials.consumer_key, credentials.consumer_secret,
                                                        credentials.access_token, credentials.access_secret)

    def start_with(self, id_name):
        bt_data_name = BTree('twitter_core_data_name', BTreeNode50String, TwitterCore, TwitterCore)
        saved_data = bt_data_name.find_first_or_default(id_name)

        if saved_data is not None:
            self.saved = saved_data.saved
            self.id = saved_data.id
            self.tweets = saved_data.tweets
            self.positive_count = saved_data.positive_count
            self.negative_count = saved_data.negative_count
        else:
            self.data_name = id_name
            dbm = DBManager(TwitterCore)
            dbm.save(self)
            bt_data_name.insert(self.data_name, self.id)

        self.twitter_stream.core_id = self.id

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
        try:
            self.twitter_stream.statuses.filter(track=tweet_track, language=tweet_language)
        except ChunkedEncodingError:
            print("Perda de conexão com o servidor")

