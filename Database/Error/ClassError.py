class Error(Exception):
    """ClassError"""
    pass


class StringWithoutSizeException(Error):
    """The give class has a string without a _size defined"""
    pass


class AttributeWithoutValidPrimitiveType(Error):
    """"Attribute with a invalid primitive type"""
    pass
