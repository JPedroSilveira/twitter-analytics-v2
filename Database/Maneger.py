import inspect
import os

_ROOT_DIR = "Database"
_DIRECTORY_SEPARATOR = "\\"
_DATABASE_DIR = "database"
_MAIN_TABLE = "main"
_ID_TABLE = "id"
_TYPE_OF_TABLE_FILE = ".dbt"

_INIT_OF_THE_FILE = 0
_ABSOLUTE_FILE_POSITION = 0
_SEPARATOR = b'"0'
_STRING_SEPARATOR = '\0'
_TYPE_SEPARATOR_START = '('
_TYPE_SEPARATOR_END = ')'
_NULL = b'0'
_ENCONDE = 'utf-8'
_MAX_SIZE = 99999


def get_database_dir():
    return "." + _DIRECTORY_SEPARATOR + _ROOT_DIR + _DIRECTORY_SEPARATOR + _DATABASE_DIR


class Maneger:

    def __init__(self, db_class):
        self.db_class = db_class
        self.db_columns = self.get_columns()
        self.class_name = db_class.__name__
        self.main_file = self.get_table_file_name(_MAIN_TABLE)
        self.id_file = self.get_table_file_name(_ID_TABLE)
        self.create_database_directory()

    def save(self, obj):
        with open(self.main_file, 'ab+') as main_file:
            ref = main_file.tell()
            obj.id = ref
            obj_bytes = self.get_serialized_obj(obj)
            main_file.write(obj_bytes)
            main_file.write(_SEPARATOR)
            print(obj.id)

    def remove_by_id(self, obj_id):
        with open(self.main_file, 'r+b') as main_file:
            main_file.seek(obj_id, _ABSOLUTE_FILE_POSITION)
            byte = b''
            last_byte = b''
            last_last_byte = b''
            count = 0
            while count < _MAX_SIZE:

                if last_last_byte == b'}' and (last_byte + byte) == _SEPARATOR:
                    break

                last_last_byte = last_byte
                last_byte = byte
                byte = main_file.read(1)
                main_file.seek(main_file.tell() - 1, _ABSOLUTE_FILE_POSITION)
                main_file.write(_NULL)
                count = count + 1

    def find_by_id(self, obj_id):
        try:
            with open(self.main_file, 'rb') as main_file:
                main_file.seek(obj_id, _ABSOLUTE_FILE_POSITION)
                byte = main_file.read(1)
                obj_bytes = b''
                last_byte = b''
                last_last_byte = b''
                count = 0
                while count < _MAX_SIZE:

                    if last_last_byte == b'}' and (last_byte + byte) == _SEPARATOR:
                        obj_bytes = obj_bytes[0:len(obj_bytes) - len(_SEPARATOR) + 1]
                        break

                    last_last_byte = last_byte
                    last_byte = byte
                    obj_bytes = obj_bytes + byte
                    byte = main_file.read(1)
                    count = count + 1
        except FileNotFoundError:
            return None

        return self.decode_serialized_obj(obj_bytes)

    def get_serialized_obj(self, obj):
        string_obj = ""

        for attr in self.get_columns():
            value = getattr(obj, attr)
            if value is not None:
                string_obj = string_obj + _STRING_SEPARATOR + _TYPE_SEPARATOR_START + type(value).__name__ \
                             + _TYPE_SEPARATOR_END + str(value)
            else:
                string_obj = string_obj + _STRING_SEPARATOR

        return bytes(string_obj, _ENCONDE)

    def decode_serialized_obj(self, bytes_obj):
        obj = self.db_class()

        string_obj = bytes.decode(bytes_obj, _ENCONDE).split(_STRING_SEPARATOR)

        for attr in self.get_columns():
            type_ = attr[1:attr.index(_TYPE_SEPARATOR_END)]

            if type_ == 'str':
                value = attr[attr.index(_TYPE_SEPARATOR_END) + 1:]
            elif type_ == 'int':
                value = int(attr[attr.index(_TYPE_SEPARATOR_END) + 1:])
            elif type_ == 'float':
                value = float(attr[attr.index(_TYPE_SEPARATOR_END) + 1:])

            setattr(obj, attr, value)

        return obj

    def get_columns(self):
        data = [a[0] for a in (inspect.getmembers(self.db_class,
                                                  lambda a: not (inspect.isroutine(a)
                                                                 or inspect.ismethod(a)
                                                                 or inspect.isfunction(a))))
                if not (a[0].startswith('__') and a[0].endswith('__'))]
        data.sort()
        return data

    def get_table_file_name(self, table_name):
        return self.get_class_database_dir() + \
               _DIRECTORY_SEPARATOR + table_name + _TYPE_OF_TABLE_FILE

    def get_class_database_dir(self):
        return get_database_dir() + _DIRECTORY_SEPARATOR + self.class_name

    def create_database_directory(self):
        if not os.path.exists(get_database_dir()):
            os.mkdir(get_database_dir())

        if not os.path.exists(self.get_class_database_dir()):
            os.mkdir(self.get_class_database_dir())
