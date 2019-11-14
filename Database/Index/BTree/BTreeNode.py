import Database.Index.BTree.BTreeCons as BTreeCons
from Database.Cons import SupportedTypes
from Database.DBData import DBData


# Default properties of any node
class BTreeNode(DBData):
    # Children_id is always a integer, refers to the id of each node
    children_ids = []
    children_ids_size = BTreeCons.KEYS_VALUES_ARRAY_SIZE * 2
    children_ids_type = SupportedTypes.INT_NAME

    # Keys saved in the tree
    # The keys type depends of each tree objective
    keys = []
    keys_size = BTreeCons.KEYS_VALUES_ARRAY_SIZE * 2 - 1

    # Content save the id of the content referenced for each tree
    # The Id type is always a integer because of the id default type in database
    # Each content refer to a key of the same position in the array
    contents = []
    contents_size = BTreeCons.KEYS_VALUES_ARRAY_SIZE * 2 - 1
    contents_type = SupportedTypes.INT_NAME

    leaf = True


# Node with integer keys
class BTreeNodeInt(BTreeNode):
    # Defines the key type of BTreeNode
    keys_type = SupportedTypes.INT_NAME

    # Function to get the node type
    @staticmethod
    def get_node_type():
        return SupportedTypes.INT_NAME
