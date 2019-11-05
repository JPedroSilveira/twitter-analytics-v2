import os

_ROOT_DIR = "Database"
_DIRECTORY_SEPARATOR = "\\"
_DATABASE_DIR = "Database"
_TYPE_OF_TABLE_FILE = ".dbt"


# FUNCTIONS

# Return the master database dir
def get_database_dir() -> str:
    return "." + _DIRECTORY_SEPARATOR + _ROOT_DIR + _DIRECTORY_SEPARATOR + _DATABASE_DIR


# Return the file of a table using its name
def get_database_file(class_name: str, file_name: str) -> str:
    return get_class_database_dir(class_name) + _DIRECTORY_SEPARATOR + file_name + _TYPE_OF_TABLE_FILE


# Return the folder of a database class
def get_class_database_dir(class_name: str) -> str:
    return get_database_dir() + _DIRECTORY_SEPARATOR + class_name


# Create the master and class folder if not exists
def create_database_directory(class_name: str):
    database_dir = get_database_dir()
    if not os.path.exists(database_dir):
        os.mkdir(database_dir)

    class_dir = get_class_database_dir(class_name)
    if not os.path.exists(class_dir):
        os.mkdir(class_dir)


def create_file(file_name: str):
    if not os.path.exists(file_name):
        buffer = open(file_name, 'w')
        buffer.close()

