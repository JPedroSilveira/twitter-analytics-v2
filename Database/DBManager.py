import Database.Cons.File as File
import Database.Cons.FileName as FileName
import Database.Helpers.DirHelper as DirHelper
import Database.Helpers.FileIndexHelper as FileIndexHelper
import Database.Helpers.ObjectHelper as ObjHelper
import Database.Helpers.ObjectReadWriteHelper as ObjectReadWriteHelper
from Database import DBData
from Database.Cons import DBTypes, Values


# Verify if a object is saved in database
from Database.Error.ReadWriteError import WritingAListBiggerThanMaxSize


def is_saved(obj):
    return obj.saved and obj.id != Values.INT_EMPTY


class DBManager:
    db_class = None
    db_columns = None
    class_name = None
    ref_class_name = None
    table_file = None
    type = None

    # Create and/or manage a table or index
    def __init__(self, db_class: type, index_name=None, index_filename=None, ref_class=None):
        if index_name:
            self.init_index(db_class, index_name, index_filename, ref_class)
        else:
            self.init_table(db_class)

    # Create and/or manage a table
    def init_table(self, db_class: type):
        self.db_class = db_class
        self.db_columns = ObjHelper.get_columns(db_class)
        self.class_name = ObjHelper.get_class_name(db_class)
        self.type = DBTypes.TABLE
        DirHelper.create_database_directory(self.class_name)
        self.table_file = DirHelper.get_database_file(self.class_name, FileName.TABLE)
        DirHelper.create_file(self.table_file)

    # Create and/or manage a index
    def init_index(self, db_class: type, index_name: str, index_filename: str, ref_class: type):
        self.db_class = db_class
        self.db_columns = ObjHelper.get_columns(db_class)
        self.class_name = index_name
        self.ref_class_name = ObjHelper.get_class_name(ref_class)
        self.type = DBTypes.INDEX
        index_dir = self.ref_class_name + '\\' + FileName.INDEX
        file_dir = index_dir + '\\' + index_name
        DirHelper.create_database_directory(self.ref_class_name)
        DirHelper.create_database_directory(index_dir)
        DirHelper.create_database_directory(file_dir)
        self.table_file = DirHelper.get_database_file(file_dir, index_filename)
        DirHelper.create_file(self.table_file)

    # Save a new record in the table
    # Return a updated object with database data like id
    def save(self, obj):
        try:
            # If already saved try to update
            if obj.saved:
                self._update(obj)
            else:  # If not save a new registry
                self._save(obj)
        except WritingAListBiggerThanMaxSize:
            return

    def _save(self, obj):
        with open(self.table_file, 'ab') as table_file:
            file_tell = table_file.tell()

        # Open in append mode
        with open(self.table_file, 'r+b') as table_file:
            table_file.seek(file_tell, File.ABSOLUTE_FILE_POSITION)
            obj.id = FileIndexHelper.get_last_id_by_file_end(self.db_class, file_tell)
            obj.saved = True
            ObjectReadWriteHelper.write_obj(table_file, obj, self.db_class)

    # Update saved data using the id
    def _update(self, obj):
        # Open in append mode
        with open(self.table_file, 'r+b') as table_file:
            seek_pos = FileIndexHelper.calculate_index_by_id(self.db_class, obj.id)
            table_file.seek(seek_pos, File.ABSOLUTE_FILE_POSITION)
            ObjectReadWriteHelper.write_obj(table_file, obj, self.db_class)

    # Find one item by id
    def find_by_id(self, obj_id: int) -> object:
        if obj_id >= 0:
            with open(self.table_file, 'rb') as table_file:
                seek_pos = FileIndexHelper.calculate_index_by_id(self.db_class, obj_id)
                table_file.seek(seek_pos, File.ABSOLUTE_FILE_POSITION)
                obj = ObjectReadWriteHelper.read_obj(table_file, self.db_class)
            return obj
        return None

    # Delete one item by id
    def delete(self, obj: DBData):
        if obj.id >= 0:
            with open(self.table_file, 'r+b') as table_file:
                seek_pos = FileIndexHelper.calculate_index_by_id(self.db_class, obj.id)
                table_file.seek(seek_pos, File.ABSOLUTE_FILE_POSITION)
                ObjectReadWriteHelper.delete_obj(table_file)

    # Drop all table if the instance type is a table or delete only the index if the instance type is an index
    def drop(self):
        if self.type == DBTypes.TABLE:
            self._drop_table()
        else:
            self._drop_index()

    # Drop a table and its contents, including indexes
    def _drop_table(self):
        DirHelper.delete_table_directory(self.class_name)

    # Drop an index
    def _drop_index(self):
        index_dir = self.ref_class_name + '\\' + FileName.INDEX
        DirHelper.delete_table_directory(index_dir)
