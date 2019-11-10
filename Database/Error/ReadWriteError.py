class Error(Exception):
    """ReadWriteError"""
    pass


class WritingANonPrimitiveType(Error):
    """The value needs to be a primite type in (int, float, str, bool)"""
    pass


class WritingAListOfInvalidType(Error):
    """The value type ins't supported for lists!"""
    pass


class ReadingAListOfInvalidType(Error):
    """The value type ins't supported for lists!"""
    pass


class WritingAListOfInvalidType(Error):
    """The value type ins't supported for lists!"""
    pass


class WritingAListWithDifferentTypes(Error):
    """A List can just have one type of variable"""


class WritingAListBiggerThanMaxSize(Error):
    """The list size is bigger than the max value sent as param"""
    pass


class ReadingANonPrimitiveType(Error):
    """The value needs to be a primite type in (int, float, str, bool)"""
    pass
