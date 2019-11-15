import Database.Helpers.ObjectHelper as ObjectHelper


# Compare each attribute of two equal objects
def compare_objs(obj_one: object, obj_two: object):
    # First verify if the classes are the same
    class_one = ObjectHelper.get_type_name(obj_one)
    class_two = ObjectHelper.get_type_name(obj_two)

    if class_one != class_two:
        return False

    attributes = ObjectHelper.get_columns(obj_one)

    # Compare each attribute to find different values
    for attr in attributes:
        value_one = ObjectHelper.get_attr_value_by_name(obj_one, attr)
        value_two = ObjectHelper.get_attr_value_by_name(obj_two, attr)

        # If different return False
        if value_one != value_two:
            return False

    # If did't find any different value then return true
    return True
