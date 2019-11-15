import Database.Index.BTree.BTreeCons as BTreeCons
from Database.Cons import SupportedTypes
from Database.DBData import DBData


# Default properties of any node
class BTreeNode(DBData):
    # Children_id is always a integer, refers to the id of each node
    children_ids = []
    children_ids_type = SupportedTypes.INT_NAME

    # If of the parent node
    parent_id = -1

    # Keys saved in the tree
    # The keys type depends of each tree objective
    keys = []

    # Content save the id of the content referenced for each tree
    # The Id type is always a integer because of the id default type in database
    # Each content refer to a key of the same position in the array
    contents = []
    contents_type = SupportedTypes.INT_NAME


# Node with integer keys
class BTreeNodeInt(BTreeNode):
    # Defines the key type of BTreeNode
    keys_type = SupportedTypes.INT_NAME

    # Defines the sized based in the degree
    children_ids_size = BTreeCons.INT_BTREE_DEGREE
    keys_size = BTreeCons.INT_BTREE_DEGREE - 1
    contents_size = BTreeCons.INT_BTREE_DEGREE - 1

    def __init__(self):
        self.children_ids = []
        self.keys = []
        self.contents = []

    # Function to get the node type
    @staticmethod
    def get_node_type():
        return SupportedTypes.INT_NAME


# Node with integer keys
class BTreeNode50String(BTreeNode):
    # Defines the key type of BTreeNode
    keys_type = SupportedTypes.STRING_NAME
    keys_size_string = 50

    # Defines the sized based in the degree
    children_ids_size = BTreeCons.STRING50_BREE_DEGREE
    keys_size = BTreeCons.STRING50_BREE_DEGREE - 1
    contents_size = BTreeCons.STRING50_BREE_DEGREE - 1

    def __init__(self):
        self.children_ids = []
        self.keys = []
        self.contents = []

    # Function to get the node type
    @staticmethod
    def get_node_type():
        return SupportedTypes.STRING_NAME
