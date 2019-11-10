# Return a read value and a bool that says if is the end of the obj
import _io
import Database.Helpers.ObjectHelper as ObjectHelper
import Database.Helpers.ReadWriteHelper as ReadWriteHelper
import Database.Cons.SupportedTypes as SupportedTypes
import Database.Cons.File as File


# Write a object starting from the set seek of the buffer
# Types with support: String, Int, Float, Boolean
def write_obj(buffer: _io.BufferedRandom, obj_class: type):
    columns = ObjectHelper.get_columns(obj_class)

    _write_exists_flag(buffer)

    for column in columns:
        if not ObjectHelper.is_info_variable(column):
            value = getattr(obj_class, column)
            column_type_name = ObjectHelper.get_type_name(getattr(obj_class, column))

            if column_type_name in SupportedTypes.COMPLEX_TYPES_NAME:
                if column_type_name == SupportedTypes.STRING_NAME:
                    max_size = ObjectHelper.get_attibute_size(obj_class, column, columns)
                    ReadWriteHelper.write_complex_value(buffer, value, max_size)
                else:
                    list_type = ObjectHelper.get_list_type_attribute(obj_class, column, columns)
                    max_size = ObjectHelper.get_attibute_size(obj_class, column, columns)
                    ReadWriteHelper.write_complex_value(buffer, value, max_size, list_type)
            else:
                ReadWriteHelper.write_primitive_value(buffer, value)


# Write the initial flag of any object
def _write_exists_flag(buffer: _io.BufferedRandom):
    ReadWriteHelper.write_bool(buffer, File.FLAG_EXISTS)


# Write the initial flag of any object with a not exists value
def _write_not_exists_flag(buffer: _io.BufferedRandom):
    ReadWriteHelper.write_bool(buffer, File.FLAG_NOT_EXISTS)


# Read a object starting from the set seek of the buffer
def read_obj(buffer: _io.BufferedRandom, obj_class: type):
    exists = ReadWriteHelper.read_bool(buffer)

    if not exists:
        return None

    obj = obj_class()

    columns = ObjectHelper.get_columns(obj_class)

    for column in columns:
        if not ObjectHelper.is_info_variable(column):
            value = getattr(obj_class, column)
            column_type_name = ObjectHelper.get_type_name(getattr(obj_class, column))

            if column_type_name in SupportedTypes.COMPLEX_TYPES_NAME:
                if column_type_name == SupportedTypes.STRING_NAME:
                    max_size = ObjectHelper.get_attibute_size(obj_class, column, columns)
                    setattr(obj, column, ReadWriteHelper.read_complex_type(buffer, value, max_size))
                else:
                    max_size = ObjectHelper.get_attibute_size(obj_class, column, columns)
                    list_type = ObjectHelper.get_list_type_attribute(obj_class, column, columns)
                    setattr(obj, column, ReadWriteHelper.read_complex_type(buffer, value, max_size, list_type))
            else:
                setattr(obj, column, ReadWriteHelper.read_primitive_type(buffer, value))

    return obj


# Delete a element from the file setting the exists flag
def delete_obj(buffer: _io.BufferedRandom):
    pos = buffer.tell()
    exists = ReadWriteHelper.read_bool(buffer)
    if exists:
        buffer.seek(pos, File.ABSOLUTE_FILE_POSITION)
        _write_not_exists_flag(buffer)