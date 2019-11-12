import Database.Error.ClassError as ClassError

# PRIMITIVE TYPE NAMES
INT_NAME = 'int'
FLOAT_NAME = 'float'
BOOL_NAME = 'bool'

# COMPLEX TYPES
STRING_NAME = 'str'
LIST_NAME = 'list'

# COMPLEX TYPES LIST
COMPLEX_TYPES_NAME = [STRING_NAME, LIST_NAME]

# TYPES ACCEPTED INSIDE A LIST
PRIMITIVE_TYPES_NAMES_FOR_LIST = [INT_NAME, FLOAT_NAME, BOOL_NAME, STRING_NAME]

# PRIMITIVE TYPE SIZES OF STRUCT PACK
FLOAT_SIZE = 8
INT_SIZE = 8
CHAR_SIZE = 1
BOOL_SIZE = 1

# SIZE VARIABLE NAME ENDS WITH:
END_OF_SIZE_VARIABLE = '_size'

# SIZE OF LIST STRING VARIABLE NAME ENDS WITH
END_OF_LIST_STRING_SIZE_VARIABLE = '_size_string'

# TYPE NAME OF THE LIST
END_OF_LIST_TYPE_VARIABLE = '_type'

# INDEX ATTRIBUTE END
END_OF_INDEX_ATTRIBUTE = '_index'

# EMPTY BINARY, NOTHING READ
EMPTY_BINARY = b''

# TYPES END
STRING_END = '\0'
BOOL_END = False
INT_END = 0
FLOAT_END = 0.0


# RETURN THE ATTRIBUTE SIZE BY NAME
def get_primitive_attribute_size_by_name(name: str) -> int:
    if name == BOOL_NAME:
        return BOOL_SIZE
    if name == INT_NAME:
        return INT_SIZE
    if name == FLOAT_NAME:
        return FLOAT_SIZE

    else:
        raise ClassError.TryingToSearchForANotSupportedAttrib(
            "Object class and column can't be none to get the attibute size of a string list")
