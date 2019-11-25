class Error(Exception):
    """ClassError"""
    pass


class SaveFunctionNotImplemented(Error):
    """It's necessary to implement a save function in every database class."""


class ChildNotFoundInDataBase(Error):
    """Child attribute need be saved in database before saving the parent!"""
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
