import pickle

_FILE_DIR = "./Database/"
_END_OF_FILE = ".db"
_INIT_OF_THE_FILE = 0
_ABSOLUTE_FILE_POSITION = 0


class DatabaseManeger:
    def __init__(self, db_class):
        self.db_class = db_class
        self.file = _FILE_DIR + db_class.__name__ + _END_OF_FILE

    def save(self, obj):
        with open(self.file, 'ab+') as file:
            obj.id = file.tell()
            pickle.dump(obj, file)

    def load(self, obj_id):
        with open(self.file, 'rb') as file:
            file.seek(obj_id, _ABSOLUTE_FILE_POSITION)
            obj = pickle.load(file)

        return obj


