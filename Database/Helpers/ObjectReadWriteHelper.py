# Return a read value and a bool that says if is the end of the obj
import _io
import Database.Helpers.ObjectHelper as ObjectHelper
import Database.Helpers.ReadWriteHelper as ReadWriteHelper
import Database.Cons.PrimitiveType as PrimitiveType
import Database.Cons.File as File


# Write a object starting from the set seek of the buffer
def write_obj(buffer: _io.BufferedRandom, obj_class: type):
    columns = ObjectHelper.get_columns(obj_class)

    _write_exists_flag(buffer)

    for column in columns:
        if not ObjectHelper.is_info_variable(column):
            value = getattr(obj_class, column)
            column_type_name = ObjectHelper.get_primitive_type_name(getattr(obj_class, column))

            if column_type_name == PrimitiveType.STRING_NAME:
                max_str_size = ObjectHelper.get_str_attibute_size(obj_class, column, columns)
                ReadWriteHelper.write_primitive_value(buffer, value, max_str_size)
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
            column_type_name = ObjectHelper.get_primitive_type_name(getattr(obj_class, column))

            if column_type_name == PrimitiveType.STRING_NAME:
                max_str_size = ObjectHelper.get_str_attibute_size(obj_class, column, columns)
                setattr(obj, column, ReadWriteHelper.read_primitive_type(buffer, value, max_str_size))
            else:
                setattr(obj, column, ReadWriteHelper.read_primitive_type(buffer, value))

    return obj


# Delete a element from the file setting the exists flag
def delete_obj(buffer: _io.BufferedRandom):
    exists = ReadWriteHelper.read_bool(buffer)
    if exists:
        _write_not_exists_flag(buffer)