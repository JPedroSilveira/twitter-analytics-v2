class Error(Exception):
    """ClassError"""
    pass


class ListOrStringWithoutSizeException(Error):
    """The give class has a string without a _size defined"""
    pass


class AttributeWithoutSizeException(Error):
    """The attribute doesn't have a size sub attribute"""
    pass


class ObjClassAndColumnAreNecessaryToGetAttributeSizeOfAStringList(Error):
    """Object Class and Column passed as None, it can't happen when you are getting the string size of a string list!"""
    pass


class TryingToSearchForANotSupportedAttributeSize(Error):
    """Typed searched are not supported!"""
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
