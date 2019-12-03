import unittest

from Data.Twitter import Tweet, Hashtag, User
from Database.Cons import Values
from Database.DBManager import DBManager
from Twitter.TwitterStreamer import AnalitycalTwitterStreamer
from Core import NaturalLanguage
from unidecode import unidecode


class JsonHashtag:
    text = Values.STRING_EMPTY

    def __init__(self, text):
        self.text = unidecode(text)


class JsonEntities:
    hashtags = []

    def __init__(self, hashtags):
        self.hashtags = []
        for hashtag in hashtags:
            self.hashtags.append(hashtag.__dict__)


class JsonUser:
    id = Values.INT_EMPTY
    name = Values.STRING_EMPTY
    location = None
    followers_count = Values.INT_EMPTY

    def __init__(self, id, name, followers_count):
        self.id = id
        self.name = unidecode(name)
        self.location = None
        self.followers_count = followers_count


class JsonTweet:
    created_at = Values.STRING_EMPTY
    id = Values.INT_EMPTY
    text = Values.STRING_EMPTY
    user = None
    entities = None

    def __init__(self, id, text, user, entities):
        self.id = id
        self.text = unidecode(text)
        self.user = user.__dict__
        self.entities = entities.__dict__
        self.created_at = "Tue Nov 26 01:50:02 +0000 2019"


class TwitterSaverTest(unittest.TestCase):

    def test_save_complete_data(self):
        hashtag_1 = JsonHashtag("TrumpAlgumaCoisa")
        hashtag_2 = JsonHashtag("ObamaAlgumaCoisa")
        hashtag_3 = JsonHashtag("LulaLivre")
        hashtag_4 = JsonHashtag("DilmaAlgumaCoisa")
        hashtag_5 = JsonHashtag("TemerAlgumaCoisa")

        entities_1 = JsonEntities([hashtag_1, hashtag_2])
        entities_2 = JsonEntities([hashtag_2, hashtag_3])
        entities_3 = JsonEntities([hashtag_3, hashtag_4])
        entities_4 = JsonEntities([hashtag_4, hashtag_5])
        entities_5 = JsonEntities([hashtag_1, hashtag_2, hashtag_3, hashtag_4, hashtag_5])

        user_1 = JsonUser(1, "Joao", 100)
        user_2 = JsonUser(2, "Alexia", 9999999)
        user_3 = JsonUser(10283820, "Trump", 4)
        user_4 = JsonUser(103910121, "Marcelo", 1018)
        user_5 = JsonUser(1827291, "Neo", 1)

        tweet_1 = JsonTweet(10182, "Aquele cara #Trump e lá #Obama!", user_1, entities_1)
        tweet_2 = JsonTweet(1183928391, "Pessoas #Obama #LulaLivre", user_2, entities_2)
        tweet_3 = JsonTweet(119283, "Tudo está um caos #Dilma #LulaLivre", user_3, entities_3)
        tweet_4 = JsonTweet(1018381, "Almoçando com meus amigos #Dilma #Temer", user_4, entities_4)
        tweet_5 = JsonTweet(1818391, "Gosto de hashtags #TrumpAlgumaCoisa #ObamaAlgumaCoisa #LulaLivre #Dilma #Temer",
                            user_5, entities_5)

        AnalitycalTwitterStreamer.on_success(None, tweet_1.__dict__)
        AnalitycalTwitterStreamer.on_success(None, tweet_2.__dict__)
        AnalitycalTwitterStreamer.on_success(None, tweet_3.__dict__)
        AnalitycalTwitterStreamer.on_success(None, tweet_4.__dict__)
        AnalitycalTwitterStreamer.on_success(None, tweet_5.__dict__)

        # Get Tweet in basic find mode
        tweetdb1 = Tweet.load(0)
        tweetdb2 = Tweet.load(1)
        tweetdb3 = Tweet.load(2)
        tweetdb4 = Tweet.load(3)
        tweetdb5 = Tweet.load(4)

        # Compare found tweets
        self.assertEqual(tweetdb1.tweet_id, tweet_1.id)
        self.assertEqual(tweetdb2.tweet_id, tweet_2.id)
        self.assertEqual(tweetdb3.tweet_id, tweet_3.id)
        self.assertEqual(tweetdb4.tweet_id, tweet_4.id)
        self.assertEqual(tweetdb5.tweet_id, tweet_5.id)
        self.assertEqual(tweetdb1.created_at, tweet_1.created_at)
        self.assertEqual(tweetdb2.created_at, tweet_2.created_at)
        self.assertEqual(tweetdb3.created_at, tweet_3.created_at)
        self.assertEqual(tweetdb4.created_at, tweet_4.created_at)
        self.assertEqual(tweetdb5.created_at, tweet_5.created_at)
        self.assertEqual(tweetdb1.text, tweet_1.text)
        self.assertEqual(tweetdb2.text, tweet_2.text)
        self.assertEqual(tweetdb3.text, tweet_3.text)
        self.assertEqual(tweetdb4.text, tweet_4.text)
        self.assertEqual(tweetdb5.text, tweet_5.text)
        self.assertEqual(tweetdb1.filtered_text, NaturalLanguage.filter_text(tweet_1.text))
        self.assertEqual(tweetdb2.filtered_text, NaturalLanguage.filter_text(tweet_2.text))
        self.assertEqual(tweetdb3.filtered_text, NaturalLanguage.filter_text(tweet_3.text))
        self.assertEqual(tweetdb4.filtered_text, NaturalLanguage.filter_text(tweet_4.text))
        self.assertEqual(tweetdb5.filtered_text, NaturalLanguage.filter_text(tweet_5.text))

        # Find User using Tweet
        userdb1 = tweetdb1.get_user()
        userdb2 = tweetdb2.get_user()
        userdb3 = tweetdb3.get_user()
        userdb4 = tweetdb4.get_user()
        userdb5 = tweetdb5.get_user()

        # Compare found users
        self.assertEqual(userdb1.twitter_id, user_1.id)
        self.assertEqual(userdb2.twitter_id, user_2.id)
        self.assertEqual(userdb3.twitter_id, user_3.id)
        self.assertEqual(userdb4.twitter_id, user_4.id)
        self.assertEqual(userdb5.twitter_id, user_5.id)
        self.assertEqual(userdb1.name, user_1.name)
        self.assertEqual(userdb2.name, user_2.name)
        self.assertEqual(userdb3.name, user_3.name)
        self.assertEqual(userdb4.name, user_4.name)
        self.assertEqual(userdb5.name, user_5.name)
        self.assertEqual(userdb1.followers_count, user_1.followers_count)
        self.assertEqual(userdb2.followers_count, user_2.followers_count)
        self.assertEqual(userdb3.followers_count, user_3.followers_count)
        self.assertEqual(userdb4.followers_count, user_4.followers_count)
        self.assertEqual(userdb5.followers_count, user_5.followers_count)
        self.assertEqual(userdb1.location, Values.STRING_EMPTY)
        self.assertEqual(userdb2.location, Values.STRING_EMPTY)
        self.assertEqual(userdb3.location, Values.STRING_EMPTY)
        self.assertEqual(userdb4.location, Values.STRING_EMPTY)
        self.assertEqual(userdb5.location, Values.STRING_EMPTY)

        hashtags_tweet_1 = tweetdb1.get_hashtags()
        hashtags_tweet_2 = tweetdb2.get_hashtags()
        hashtags_tweet_3 = tweetdb3.get_hashtags()
        hashtags_tweet_4 = tweetdb4.get_hashtags()
        hashtags_tweet_5 = tweetdb5.get_hashtags()

        # Compare hashtag data
        for hashtag in hashtags_tweet_1:
            self.assertTrue(hashtag.text in [hashtag_1.text, hashtag_2.text])
            self.assertFalse(hashtag.text in [hashtag_3.text, hashtag_4.text, hashtag_5.text])
        for hashtag in hashtags_tweet_2:
            self.assertTrue(hashtag.text in [hashtag_2.text, hashtag_3.text])
            self.assertFalse(hashtag.text in [hashtag_1.text, hashtag_4.text, hashtag_5.text])
        for hashtag in hashtags_tweet_3:
            self.assertTrue(hashtag.text in [hashtag_3.text, hashtag_4.text])
            self.assertFalse(hashtag.text in [hashtag_1.text, hashtag_2.text, hashtag_5.text])
        for hashtag in hashtags_tweet_4:
            self.assertTrue(hashtag.text in [hashtag_4.text, hashtag_5.text])
            self.assertFalse(hashtag.text in [hashtag_1.text, hashtag_2.text, hashtag_3.text])
        for hashtag in hashtags_tweet_5:
            self.assertTrue(hashtag.text in [hashtag_1.text, hashtag_2.text,
                                             hashtag_3.text, hashtag_4.text, hashtag_5.text])


        # Get Hashtags in basic find mode
        hashtagdb1 = Hashtag.load(0)
        hashtagdb2 = Hashtag.load(1)
        hashtagdb3 = Hashtag.load(2)
        hashtagdb4 = Hashtag.load(3)
        hashtagdb5 = Hashtag.load(4)

        tweets_hashtag_bd_1 = hashtagdb1.get_tweets()
        tweets_hashtag_bd_2 = hashtagdb2.get_tweets()
        tweets_hashtag_bd_3 = hashtagdb3.get_tweets()
        tweets_hashtag_bd_4 = hashtagdb4.get_tweets()
        tweets_hashtag_bd_5 = hashtagdb5.get_tweets()

        # Compare tweets data
        self.assertTrue(len(tweets_hashtag_bd_1) == 2)
        self.assertTrue(len(tweets_hashtag_bd_2) == 3)
        self.assertTrue(len(tweets_hashtag_bd_3) == 3)
        self.assertTrue(len(tweets_hashtag_bd_4) == 3)
        self.assertTrue(len(tweets_hashtag_bd_5) == 2)

        for tweet in tweets_hashtag_bd_1:
            self.assertTrue(tweet.id in [0, 4])
        for tweet in tweets_hashtag_bd_2:
            self.assertTrue(tweet.id in [0, 1, 4])
        for tweet in tweets_hashtag_bd_3:
            self.assertTrue(tweet.id in [1, 2, 4])
        for tweet in tweets_hashtag_bd_4:
            self.assertTrue(tweet.id in [2, 3, 4])
        for tweet in tweets_hashtag_bd_5:
            self.assertTrue(tweet.id in [3, 4])

        # Get Users in basic find mode
        userdb1 = User.load(0)
        userdb2 = User.load(1)
        userdb3 = User.load(2)
        userdb4 = User.load(3)
        userdb5 = User.load(4)

        # Compare found users
        self.assertEqual(userdb1.twitter_id, user_1.id)
        self.assertEqual(userdb2.twitter_id, user_2.id)
        self.assertEqual(userdb3.twitter_id, user_3.id)
        self.assertEqual(userdb4.twitter_id, user_4.id)
        self.assertEqual(userdb5.twitter_id, user_5.id)
        self.assertEqual(userdb1.name, user_1.name)
        self.assertEqual(userdb2.name, user_2.name)
        self.assertEqual(userdb3.name, user_3.name)
        self.assertEqual(userdb4.name, user_4.name)
        self.assertEqual(userdb5.name, user_5.name)
        self.assertEqual(userdb1.followers_count, user_1.followers_count)
        self.assertEqual(userdb2.followers_count, user_2.followers_count)
        self.assertEqual(userdb3.followers_count, user_3.followers_count)
        self.assertEqual(userdb4.followers_count, user_4.followers_count)
        self.assertEqual(userdb5.followers_count, user_5.followers_count)
        self.assertEqual(userdb1.location, Values.STRING_EMPTY)
        self.assertEqual(userdb2.location, Values.STRING_EMPTY)
        self.assertEqual(userdb3.location, Values.STRING_EMPTY)
        self.assertEqual(userdb4.location, Values.STRING_EMPTY)
        self.assertEqual(userdb5.location, Values.STRING_EMPTY)

        user_tweets_1 = userdb1.get_tweets()
        user_tweets_2 = userdb2.get_tweets()
        user_tweets_3 = userdb3.get_tweets()
        user_tweets_4 = userdb4.get_tweets()
        user_tweets_5 = userdb5.get_tweets()

        # Compare found tweets
        self.assertEqual(user_tweets_1[0].tweet_id, tweet_1.id)
        self.assertEqual(user_tweets_2[0].tweet_id, tweet_2.id)
        self.assertEqual(user_tweets_3[0].tweet_id, tweet_3.id)
        self.assertEqual(user_tweets_4[0].tweet_id, tweet_4.id)
        self.assertEqual(user_tweets_5[0].tweet_id, tweet_5.id)
        self.assertEqual(user_tweets_1[0].created_at, tweet_1.created_at)
        self.assertEqual(user_tweets_2[0].created_at, tweet_2.created_at)
        self.assertEqual(user_tweets_3[0].created_at, tweet_3.created_at)
        self.assertEqual(user_tweets_4[0].created_at, tweet_4.created_at)
        self.assertEqual(user_tweets_5[0].created_at, tweet_5.created_at)

        manager = DBManager(Hashtag)
        manager.drop()
        manager = DBManager(Tweet)
        manager.drop()
        manager = DBManager(User)
        manager.drop()










if __name__ == '__main__':
    unittest.main()
