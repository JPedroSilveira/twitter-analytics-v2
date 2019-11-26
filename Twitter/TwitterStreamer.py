from twython import TwythonStreamer

from Data.Twitter import Hashtag
from Data.Twitter import Tweet
from Data.Twitter import User


class AnalitycalTwitterStreamer(TwythonStreamer):

    def on_success(self, data):
        tweet = Tweet()
        success = tweet.set(data)

        if success:
            print("Saving tweet:" + tweet.text)
            if tweet.find_self() is None:
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
                    tweet.db_save()

                    for hashtag in hashtags:
                        hashtag.add_tweet(tweet)

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
