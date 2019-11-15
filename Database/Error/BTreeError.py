class Error(Exception):
    """BTreeError"""
    pass


class OneMoreChildThanDataRequired(Error):
    """One more child than data item required"""
    pass
