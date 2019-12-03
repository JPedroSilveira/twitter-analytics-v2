from Core import NaturalLanguage
from Database.DBManager import DBManager
from Database import DBManager as DBM
from Database.Cons import Values
from Database.DBData import DBData
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNode280String, BTreeNode50String


class WorldDS(DBData):
    total_positive = 0
    total_negative = 0

    def add_positive(self):
        self.total_positive = self.total_positive + 1

    def add_negative(self):
        self.total_negative = self.total_negative + 1

    def db_save(self):
        dbm = DBManager(WorldDS)
        dbm.save(self)

    def load(id):
        dbm = DBManager(WorldDS)
        return dbm.find_by_id(0)

    def db_delete(self):
        if DBM.is_saved(self):
            dbm = DBManager(WorldDS)
            dbm.delete(self)


class TweetDS(DBData):
    text = Values.STRING_EMPTY
    text_size = 280
    negative = False

    def __init__(self, text, negative):
        self.text = NaturalLanguage.filter_text(text)
        self.negative = negative

    def db_save(self):
        if not DBManager:
            dbm = DBManager(TweetDS)
            dbm.save(self)

            tweet_dataset_text_id = BTree('tweet_dataset_text_id', BTreeNode280String, TweetDS, TweetDS)
            tweet_dataset_text_id.insert(self.text, self.id)

    # Return the words without repeat
    # Bernoulli model: just present or not present
    def get_words(self):
        not_empty_words = list(filter(lambda x: x != '', self.text.split(' ')))
        return list(dict.fromkeys(not_empty_words))

    def load(id: int):
        dbm = DBManager(TweetDS)
        return dbm.find_by_id(id)

    def load_by_text(text: str):
        tweet_dataset_text_id = BTree('tweet_dataset_text_id', BTreeNode280String, TweetDS, TweetDS)
        return tweet_dataset_text_id.find_first_or_default(NaturalLanguage.filter_text(text))

    def db_delete(self):
        if DBM.is_saved(self):
            dbm = DBManager(TweetDS)
            dbm.delete(self)


class WordDS(DBData):
    text = Values.STRING_EMPTY
    text_size = 50

    n_positive = 0
    n_negative = 0

    # Ever use filtered text by TweetDS
    def __init__(self, text=None):
        if text is not None:
            self.text = text

    def add_negative(self):
        self.n_negative = self.n_negative + 1

    def add_positive(self):
        self.n_positive = self.n_positive + 1

    def db_save(self):
        saved = False
        if DBM.is_saved(self):
            saved = True

        dbm = DBManager(WordDS)
        dbm.save(self)

        if not saved:
            word_dataset_text_id = BTree('word_dataset_text_id', BTreeNode50String, WordDS, WordDS)
            word_dataset_text_id.insert(self.text, self.id)

    def load(id):
        dbm = DBManager(WordDS)
        return dbm.find_by_id(id)

    # Ever use filtered text by TweetDS
    def load_by_text(text):
        word_dataset_text_id = BTree('word_dataset_text_id', BTreeNode50String, WordDS, WordDS)
        return word_dataset_text_id.find_first_or_default(text)

    def db_delete(self):
        if DBM.is_saved(self):
            dbm = DBManager(WordDS)
            dbm.delete(self)
