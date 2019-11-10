class Error(Exception):
    """ClassError"""
    pass


class ListOrStringWithoutSizeException(Error):
    """The give class has a string without a _size defined"""
    pass


class AttributeWithoutSizeException(Error):
    """The attribute doesn't have a size sub attribute"""


class AttributeWithoutTypeException(Error):
    """The attribute doesn't have a type sub attribute"""


class AttributeSizeOfListCantBeNone(Error):
    """The attribute size can't be none"""


class AttributeTypeWithoutSize(Error):
    """This type of attribute can't use a size attribute"""


class AttributeWithoutValidPrimitiveType(Error):
    """"Attribute with a invalid primitive type"""
    pass
