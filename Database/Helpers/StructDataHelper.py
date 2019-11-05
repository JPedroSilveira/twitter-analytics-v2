import struct
import Database.Cons.Encode as Encode
import Database.Cons.PrimitiveType as PrimitiveType


# FUNCTIONS -> CONVERT TO BINARY

# Convert a python float to a binary struct double
def convert_to_bin_double(value: float) -> bytes:
    return struct.pack('d', value)


# Convert a python int to a binary struct int
def convert_to_bin_int(value: int) -> bytes:
    return struct.pack('q', value)


# Convert a python string of length 1 to a binary struct char
# value = Encoded string
def convert_to_bin_char(value: bytes) -> bytes:
    return struct.pack('c', value.encode(Encode.DEFAULT_STR_ENCONDE))


# Convert a python int to a binary struct int
def convert_to_bin_bool(value: bool) -> bytes:
    return struct.pack('b', value)


# FUNCTIONS -> CONVERT FROM BINARY

# Convert a binary struct double to a python float
def convert_from_bin_double(value: bytes) -> float:
    return struct.unpack('d', value)[0]


# Convert a binary struct int to a python int
def convert_from_bin_int(value: bytes) -> int:
    return struct.unpack('q', value)[0]


# Convert a binary struct char to a python string of length 1
def convert_from_bin_char(value: bytes) -> str:
    return (struct.unpack('c', value.encode(Encode.DEFAULT_STR_ENCONDE))[0]).decode(Encode.DEFAULT_STR_ENCONDE)


# Convert a binary struct int to a python int
def convert_from_bin_bool(value: bytes) -> bool:
    # Exception: if read empty in bool mode return False
    if value == PrimitiveType.EMPTY_BINARY:
        return False

    return struct.unpack('b', value)[0] == 1
