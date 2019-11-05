class Error(Exception):
    """ReadWriteError"""
    pass


class WritingANonPrimitiveType(Error):
    """The value needs to be a primite type in (int, float, str, bool)"""
    pass


class ReadingANonPrimitiveType(Error):
    """The value needs to be a primite type in (int, float, str, bool)"""
    pass
