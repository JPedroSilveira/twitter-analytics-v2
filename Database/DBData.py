from Database.Cons import Values
from Database.Error import ClassError


class DBData(object):
    id = Values.INT_EMPTY
    saved = False

    # Used for do some stuff after database load
    @staticmethod
    def initialize():
        return None

    def db_save(self):
        raise ClassError.SaveFunctionNotImplemented("It's necessary to implement db_save in all database entities!")
