import msvcrt

from twython import TwythonStreamer

from Data.Twitter import Hashtag
from Data.Twitter import Tweet
from Data.Twitter import User
from Database.DBManager import DBManager
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNodeInt, BTreeNodeFloat, BTreeNode50String, BTreeNode50IntString
from Twitter import TwitterCore


class AnalitycalTwitterStreamer(TwythonStreamer):
    core_id = 0

    def on_success(self, data):
        tweet = Tweet()
        success = tweet.set(data)
        ignore = False

        if success:
            try:
                print("Saving tweet: " + tweet.text)
            except OSError:
                ignore = True

            if tweet.find_self() is None and not ignore:
                user = User()
                success = user.set(data['user'])
                hashtags = []
                if success:
                    user.find_self()
                    user.db_save()

                    for hashtag_data in data['entities']['hashtags']:
                        hashtag = Hashtag()
                        success = hashtag.set(hashtag_data)
                        if success:
                            hashtags.append(hashtag)
                            if hashtag.find_self() is None:
                                hashtag.db_save()

                    tweet.set_hashtags(hashtags)
                    tweet.set_user(user)
                    tweet.infer()
                    tweet.db_save()

                    dbm = DBManager(TwitterCore.TwitterCore)
                    core = dbm.find_by_id(self.core_id)
                    core.tweets = core.tweets + 1

                    if tweet.negative:
                        core.negative_count = core.negative_count + 1
                    else:
                        core.positive_count = core.positive_count + 1

                    dbm.save(core)

                    bt_core_tweets = BTree('twitter_core_tweets', BTreeNodeInt, TwitterCore, Tweet)
                    bt_core_tweets.insert(core.id, tweet.id)

                    bt_core_tweets.insert(core.id, tweet.id)

                    if tweet.negative:
                        bt_core_most_negative = BTree('twitter_core_most_negative_' + core.data_name,
                                                  BTreeNodeFloat, TwitterCore, Tweet)

                        bt_core_most_negative.insert(tweet.negative_score, tweet.id)

                    else:
                        bt_core_most_positive = BTree('twitter_core_most_positive_' + core.data_name,
                                                  BTreeNodeFloat, TwitterCore, Tweet)

                        bt_core_most_positive.insert(tweet.positive_score, tweet.id)

                    words = tweet.get_filtered_words()

                    if tweet.negative:
                        bt_core_most_negative_words_main = BTree('bt_core_most_negative_words_main_' + core.data_name,
                                                                 BTreeNode50String, TwitterCore)
                        bt_core_most_negative_words = BTree('bt_core_most_negative_words' + core.data_name,
                                                            BTreeNode50IntString, TwitterCore)

                        for word in words:
                            negative_count = bt_core_most_negative_words_main.find_first_or_default(word)

                            if negative_count is not None:
                                bt_core_most_negative_words.delete(negative_count, word)
                                bt_core_most_negative_words.insert(negative_count + 1, word)
                                bt_core_most_negative_words_main.delete(word, negative_count)
                                bt_core_most_negative_words_main.insert(word, negative_count + 1)
                            else:
                                bt_core_most_negative_words_main.insert(word, 1)
                                bt_core_most_negative_words.insert(1, word)

                    else:
                        bt_core_most_positive_words_main = BTree('bt_core_most_positive_words_main_' + core.data_name,
                                                                 BTreeNode50String, TwitterCore)
                        bt_core_most_positive_words = BTree('bt_core_most_positive_words' + core.data_name,
                                                            BTreeNode50IntString, TwitterCore)

                        for word in words:
                            positive_count = bt_core_most_positive_words_main.find_first_or_default(word)

                            if positive_count is not None:
                                bt_core_most_positive_words.delete(positive_count, word)
                                bt_core_most_positive_words.insert(positive_count + 1, word)
                                bt_core_most_positive_words_main.delete(word, positive_count)
                                bt_core_most_positive_words_main.insert(word, positive_count + 1)
                            else:
                                bt_core_most_positive_words_main.insert(word, 1)
                                bt_core_most_positive_words.insert(1, word)

                    for hashtag in hashtags:
                        hashtag.add_tweet(tweet)

        if self.verify_end_option():
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    def on_timeout(self):
        print('Connection timeout')
        self.disconnect()

    def verify_end_option(self) -> bool:
        if msvcrt.kbhit():
            if msvcrt.getch() == b'c' or msvcrt.getch() == b'C':
                return True

        return False
