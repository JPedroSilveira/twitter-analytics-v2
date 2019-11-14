import Database.Index.BTree.BTreeCons as BTreeCons
from Database.Cons import SupportedTypes
from Database.DBData import DBData


# Use
# >>> import io
# >>> io.DEFAULT_BUFFER_SIZE
# to know the default buffer of Python for your OS.
# You can use this how a way to calculate the ideal size of the keys array.
class BTreeNodeInt(DBData):
    id = 0

    # Children_id is always a integer, refers to the id of each node
    children_id = []
    children_id_size = BTreeCons.KEYS_VALUES_ARRAY_SIZE * 2
    children_id_type = SupportedTypes.INT_NAME

    # Keys saved in the tree
    # The keys type depends of each tree objective
    keys = []
    keys_size = BTreeCons.KEYS_VALUES_ARRAY_SIZE * 2 - 1
    keys_type = SupportedTypes.INT_NAME

    # Content save the id of the content referenced for each tree
    # The Id type is always a integer because of the id default type in database
    # Each content refer to a key of the same position in the array
    content = []
    content_size = BTreeCons.KEYS_VALUES_ARRAY_SIZE * 2 - 1
    content_type = SupportedTypes.INT_NAME

    leaf = True

    @staticmethod
    def get_node_type():
        return SupportedTypes.INT_NAME
