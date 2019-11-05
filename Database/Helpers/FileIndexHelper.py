import Database.Helpers.ObjectHelper as ObjectHelper


# Return the last id of the current file using the file end and the class
def get_last_id_by_file_end(obj_class: type, file_end: int) -> int:
    obj_size = ObjectHelper.get_class_size(obj_class)

    return int(file_end / obj_size)


def calculate_index_by_id(obj_class: type, obj_id: int) -> int:
    obj_size = ObjectHelper.get_class_size(obj_class)

    return obj_id * obj_size
