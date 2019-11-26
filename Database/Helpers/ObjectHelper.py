import inspect

import Database.Cons.File as File
import Database.Cons.SupportedTypes as SupportedTypes
import Database.Error.ClassError as ClassError


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
    name = obj_class.__name__
    point_pos = name.find(".")
    while point_pos >= 0 and len(name) > point_pos + 1:
        name = name[point_pos + 1:]
        point_pos = name.find(".")

    return name


# Return the name of the primitive type of a attribute
def get_type_name(attribute) -> str:
    return type(attribute).__name__


# Return the storage size in bytes of a class
def get_class_size(obj_class: type) -> int:
    columns = get_columns(obj_class)
    size = 0

    for column in columns:
        if not is_info_variable(column):
            size = size + get_column_size(obj_class, column)

    # Sum the size of exists flag
    return size + SupportedTypes.get_primitive_attribute_size_by_name(get_type_name(File.FLAG_EXISTS))


# Return the size of a supported type in a obj
def get_column_size(obj_class: type, column: str) -> int:
    column_type_name = get_type_name(getattr(obj_class, column))

    if column_type_name == SupportedTypes.INT_NAME:
        return SupportedTypes.INT_SIZE

    if column_type_name == SupportedTypes.FLOAT_NAME:
        return SupportedTypes.FLOAT_SIZE

    if column_type_name == SupportedTypes.BOOL_NAME:
        return SupportedTypes.BOOL_SIZE

    if column_type_name == SupportedTypes.STRING_NAME:
        return get_attribute_size(obj_class, column) * SupportedTypes.CHAR_SIZE

    if column_type_name == SupportedTypes.LIST_NAME:
        list_type = get_list_type_attribute(obj_class, column)

        if list_type == SupportedTypes.STRING_NAME:
            list_type_size = get_attribute_list_string_size(obj_class, column)
        else:
            list_type_size = SupportedTypes.get_primitive_attribute_size_by_name(list_type)

        if list_type_size is None:
            raise ClassError.AttributeWithoutValidPrimitiveType(
                'Class ' + obj_class + ' has a list with not property type')

        list_size = get_attribute_size(obj_class, column)

        # Check if the attribute size have been sent
        if list_size is None:
            raise ClassError.AttributeSizeOfListCantBeNone('Class ' + obj_class + ' has a not supported type!')

        # The size of a list is the size of each element multiplied by the list max size plus a
        # int size that is used to save the real list size
        return list_size * list_type_size + SupportedTypes.INT_SIZE

    raise ClassError.AttributeWithoutValidPrimitiveType('Class has an attribute swith a invalid type!')


def get_list_type_attribute(obj_class: type, column: str):
    list_type_attribute = column + SupportedTypes.END_OF_LIST_TYPE_VARIABLE

    return get_attr_value_by_name(obj_class, list_type_attribute)


# Return value of the attribute with the string or list max size
def get_attribute_size(obj_class: type, column: str) -> int:
    size_attribute = column + SupportedTypes.END_OF_SIZE_VARIABLE

    return get_attr_value_by_name(obj_class, size_attribute)


def get_attribute_list_string_size(obj_class: type, column: str) -> int:
    size_attribute = column + SupportedTypes.END_OF_LIST_STRING_SIZE_VARIABLE

    return get_attr_value_by_name(obj_class, size_attribute)


# Return if the column is a info variable that can't be saved in database
def is_info_variable(column: str):
    return (column.endswith(SupportedTypes.END_OF_SIZE_VARIABLE)
            or column.endswith(SupportedTypes.END_OF_LIST_TYPE_VARIABLE)
            or column.endswith(SupportedTypes.END_OF_INDEX_ATTRIBUTE)
            or column.endswith(SupportedTypes.END_OF_LIST_STRING_SIZE_VARIABLE))


def get_attr_value_by_name(obj_class: object, column: str):
    columns = get_columns(obj_class)
    size_attr_list = list(filter(lambda x: x == column, columns))

    # Verify if found any size attribute
    if len(size_attr_list) == 0:
        raise ClassError.AttributeNotFound('Class ' + obj_class + 'has no attribute ' + column + '!')

    return getattr(obj_class, size_attr_list[0])
