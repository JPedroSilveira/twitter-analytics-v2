import _io
import re
import Database.Helpers.StructDataHelper as StructDataHelper
import Database.Helpers.ObjectHelper as ObjectHelper
import Database.Cons.PrimitiveType as PrimitiveType
import Database.Error.ReadWriteError as ReadWriteError
import Database.Cons.File as File
import Database.Cons.Encode as Encode

_STRING_SIZE_NAME = '_size'
_STRING_END = '\0'


# WRITE FUNCTIONS: WRITE A TYPED VALUE WITH A BUFFER
def write_primitive_value(buffer: _io.BufferedRandom, value, max_str_size=0):
    prim_type_name = ObjectHelper.get_primitive_type_name(value)

    if prim_type_name == PrimitiveType.INT_NAME:
        write_int(buffer, value)

    elif prim_type_name == PrimitiveType.FLOAT_NAME:
        write_float(buffer, value)

    elif prim_type_name == PrimitiveType.BOOL_NAME:
        write_bool(buffer, value)

    elif prim_type_name == PrimitiveType.STRING_NAME:
        write_str(buffer, value, max_str_size)

    else:
        raise ReadWriteError.WritingANonPrimitiveType('Value ' + value + ' can\'t be a non primitive type!')


def write_int(buffer: _io.BufferedRandom, value: int):
    buffer.write(StructDataHelper.convert_to_bin_int(value))


def write_float(buffer: _io.BufferedRandom, value: float):
    buffer.write(StructDataHelper.convert_to_bin_double(value))


def write_str(buffer: _io.BufferedRandom, value: str, max_size: int):
    stop_count = 0
    value = _remove_invalid_char(value)

    for char in value:
        if stop_count == max_size:
            break

        buffer.write(StructDataHelper.convert_to_bin_char(char))

        stop_count = stop_count + 1

    # Complete the string size with zeros
    while stop_count != max_size:
        buffer.write(StructDataHelper.convert_to_bin_char(_STRING_END))
        stop_count = stop_count + 1


def _remove_invalid_char(value: str) -> str:
    return re.sub(r'[^\x00-\x7f]', r' ', value)


def write_bool(buffer: _io.BufferedRandom, value: bool):
    buffer.write(StructDataHelper.convert_to_bin_bool(value))


# READ FUNCTIONS: READ A TYPED VALUE WITH A BUFFER
def read_primitive_type(buffer: _io.BufferedRandom, value, max_size=0):
    prim_type_name = ObjectHelper.get_primitive_type_name(value)

    if prim_type_name == PrimitiveType.INT_NAME:
        return read_int(buffer)

    if prim_type_name == PrimitiveType.FLOAT_NAME:
        return read_float(buffer)

    if prim_type_name == PrimitiveType.BOOL_NAME:
        return read_bool(buffer)

    if prim_type_name == PrimitiveType.STRING_NAME:
        return read_str(buffer, max_size)

    raise ReadWriteError.ReadingANonPrimitiveType('Type ' + prim_type_name + ' ins\'t a valid non primitive type!')


def read_int(buffer: _io.BufferedRandom) -> int:
    return StructDataHelper.convert_from_bin_int(buffer.read(PrimitiveType.INT_SIZE))


def read_float(buffer: _io.BufferedRandom) -> float:
    return StructDataHelper.convert_from_bin_double(buffer.read(PrimitiveType.DOUBLE_SIZE))


def read_bool(buffer: _io.BufferedRandom) -> bool:
    return StructDataHelper.convert_from_bin_bool(buffer.read(PrimitiveType.BOOL_SIZE))


def read_str(buffer: _io.BufferedRandom, max_size: int) -> str:
    value = ''
    char_count = 0

    # Remove one of the string end \0
    while char_count < max_size - 1:
        new_char = StructDataHelper.convert_from_bin_char(buffer.read(PrimitiveType.CHAR_SIZE))

        # \0 is the end
        if new_char == _STRING_END:
            break

        value = value + new_char
        char_count = char_count + 1

    # Place the buffer in the end of the string
    if char_count != max_size:
        buffer.seek(buffer.tell() + max_size - char_count - 1, File.ABSOLUTE_FILE_POSITION)

    return value
