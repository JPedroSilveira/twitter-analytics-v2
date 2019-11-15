class DBData(object):
    id = 0
    saved = False

    # Used for do some stuff after database load
    @staticmethod
    def initialize():
        return None
