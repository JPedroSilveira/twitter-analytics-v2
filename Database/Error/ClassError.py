class Error(Exception):
    """ClassError"""
    pass


class AttributeNotFound(Error):
    """Attribute not found in the class"""
    pass


class AttributeWithoutTypeException(Error):
    """The attribute doesn't have a type sub attribute"""
    pass


class AttributeSizeOfListCantBeNone(Error):
    """The attribute size can't be none"""
    pass


class AttributeTypeWithoutSize(Error):
    """This type of attribute can't use a size attribute"""
    pass


class AttributeWithoutValidPrimitiveType(Error):
    """"Attribute with a invalid primitive type"""
    pass
