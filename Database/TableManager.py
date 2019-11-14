import Database.Cons.File as File
import Database.Cons.FileName as FileName
import Database.Helpers.DirHelper as DirHelper
import Database.Helpers.FileIndexHelper as FileIndexHelper
import Database.Helpers.ObjectHelper as ObjHelper
import Database.Helpers.ObjectReadWriteHelper as ObjectReadWriteHelper


class TableManager:

    db_class = None
    db_columns = None
    class_name = None
    ref_class_name = None
    table_file = None

    # Create and/or manage a table or index
    def __init__(self, db_class: type, index_name: str, index_filename: str, ref_class=None):
        if index_name:
            self.init_index(db_class, index_name, index_filename, ref_class)
        else:
            self.init_table(db_class)

    # Create and/or manage a table
    def init_table(self, db_class: type):
        self.db_class = db_class
        self.db_columns = ObjHelper.get_columns(db_class)
        self.class_name = ObjHelper.get_class_name(db_class)
        DirHelper.create_database_directory(self.class_name)
        self.table_file = DirHelper.get_database_file(self.class_name, FileName.TABLE)
        DirHelper.create_file(self.table_file)

    # Create and/or manage a index
    def init_index(self, db_class: type, index_name: str, index_filename: str, ref_class: type):
        self.db_class = db_class
        self.db_columns = ObjHelper.get_columns(db_class)
        self.class_name = index_name
        self.ref_class_name = ObjHelper.get_class_name(ref_class)
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
        with open(self.table_file, 'ab') as table_file:
            file_tell = table_file.tell()

        # Open in append mode
        with open(self.table_file, 'r+b') as table_file:
            table_file.seek(file_tell, File.ABSOLUTE_FILE_POSITION)
            obj.id = FileIndexHelper.get_last_id_by_file_end(self.db_class, file_tell)
            ObjectReadWriteHelper.write_obj(table_file, obj, self.db_class)

    def update(self, obj):
        # Open in append mode
        with open(self.table_file, 'r+b') as table_file:
            seek_pos = FileIndexHelper.calculate_index_by_id(self.db_class, obj.id)
            table_file.seek(seek_pos, File.ABSOLUTE_FILE_POSITION)
            ObjectReadWriteHelper.write_obj(table_file, obj, self.db_class)

    def find_by_id(self, obj_id: int) -> object:
        with open(self.table_file, 'rb') as table_file:
            seek_pos = FileIndexHelper.calculate_index_by_id(self.db_class, obj_id)
            table_file.seek(seek_pos, File.ABSOLUTE_FILE_POSITION)
            obj = ObjectReadWriteHelper.read_obj(table_file, self.db_class)
            # TO-DO: Erro ao salvar BTree main
        return obj

    def delete_by_id(self, obj_id: int) -> object:
        with open(self.table_file, 'r+b') as table_file:
            seek_pos = FileIndexHelper.calculate_index_by_id(self.db_class, obj_id)
            table_file.seek(seek_pos, File.ABSOLUTE_FILE_POSITION)
            ObjectReadWriteHelper.delete_obj(table_file)
