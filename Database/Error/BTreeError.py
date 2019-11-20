class Error(Exception):
    """BTreeError"""
    pass


class OneMoreChildThanDataRequired(Error):
    """One more child than data item required"""
    pass


class NodeWithoutSiblings(Error):
    """Every node, except the root needs to have siblings"""
    pass
