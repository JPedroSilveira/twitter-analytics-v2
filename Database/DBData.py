class DBData(object):
    id = -1
    saved = False

    # Used for do some stuff after database load
    @staticmethod
    def initialize():
        return None
