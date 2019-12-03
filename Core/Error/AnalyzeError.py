class Error(Exception):
    """AnalyzeError"""
    pass


class TryingToInferWithoutWorldData(Error):
    """First you need to train the program with some data!"""
    pass