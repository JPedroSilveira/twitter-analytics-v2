import inspect
import Database.Cons.PrimitiveType as PrimitiveType
import Database.Error.ClassError as ClassError
import Database.Cons.File as File


# FUNCTIONS

# Return a list with the columns name of a object
def get_columns(obj_class: type) -> list:
    data = [a[0] for a in (inspect.getmembers(obj_class,
                                              lambda a: not (inspect.isroutine(a)
                                                             or inspect.ismethod(a)
                                                             or inspect.isfunction(a))))
            if not (a[0].startswith('__') and a[0].endswith('__'))]
    data.sort()

    return data


# Return the name of the class
def get_class_name(obj_class: type) -> str:
    return obj_class.__name__


# Return the name of the primitive type of a attribute
def get_primitive_type_name(attribute) -> str:
    return type(attribute).__name__


# Return the storage size in bytes of a class
def get_class_size(obj_class: type) -> int:
    columns = get_columns(obj_class)
    size = 0

    for column in columns:
        if not is_info_variable(column):
            size = size + get_primitive_column_size(obj_class, column, columns)

    # Sum the size of exists flag
    return size + File.FLAG_EXISTS_SIZE


# Return the size of a primitive type or a string in a obj
def get_primitive_column_size(obj_class: type, column: str, columns: list) -> int:
    column_type_name = get_primitive_type_name(getattr(obj_class, column))

    if column_type_name == PrimitiveType.INT_NAME:
        return PrimitiveType.INT_SIZE

    if column_type_name == PrimitiveType.FLOAT_NAME:
        return PrimitiveType.DOUBLE_SIZE

    if column_type_name == PrimitiveType.BOOL_NAME:
        return PrimitiveType.BOOL_SIZE

    if column_type_name == PrimitiveType.STRING_NAME:
        return get_str_attibute_size(obj_class, column, columns)

    raise ClassError.AttributeWithoutValidPrimitiveType('Class ' + obj_class + ' has a attribute ' + column +
                                                        ' with a invalid type!')


# Return value of the attribute with the string size
def get_str_attibute_size(obj_class: type, column: str, columns: list) -> int:
    str_size_attribute = column + PrimitiveType.END_OF_STRING_SIZE_VARIABLE
    size_attr_list = list(filter(lambda x: x == str_size_attribute, columns))

    if len(size_attr_list) == 0:
        raise ClassError.StringWithoutSizeException('Class ' + obj_class + ' has no attribute ' +
                                                    str_size_attribute + ' with the max size of ' + column + '!')

    # Add one of the end char
    return (getattr(obj_class, size_attr_list[0]) + 1) * PrimitiveType.CHAR_SIZE


# Return if the column is a info variable that can't be saved in database
def is_info_variable(column: str):
    return column.endswith(PrimitiveType.END_OF_STRING_SIZE_VARIABLE)
