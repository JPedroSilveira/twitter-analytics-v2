from Database import TableManager
from Database.Cons import SupportedTypes, FileName

_KEYS_VALUES_ARRAY_SIZE = 80


# Use
# >>> import io
# >>> io.DEFAULT_BUFFER_SIZE
# to know the default buffer of Python for your OS.
# You can use this how a way to calculate the ideal size of the keys array.
class BTreeNodeInt:
    id = 0

    # Children_id is always a integer, refers to the id of each node
    children_id = []
    children_id_size = _KEYS_VALUES_ARRAY_SIZE * 2 + 1
    children_id_type = SupportedTypes.INT_NAME

    # Keys saved in the tree
    # The keys type depends of each tree objective
    keys = []
    keys_size = _KEYS_VALUES_ARRAY_SIZE * 2
    keys_type = SupportedTypes.INT_NAME

    # Content save the id of the content referenced for each tree
    # The Id type is always a integer because of the id default type in database
    # Each content refer to a key of the same position in the array
    content = []
    content_size = _KEYS_VALUES_ARRAY_SIZE * 2
    content_type = SupportedTypes.INT_NAME

    leaf = True

    @staticmethod
    def get_node_type():
        return SupportedTypes.INT_NAME


class BTree:
    # Id of the root
    root_id = 0

    def __init__(self, index_name: str, node_class: object):
        # Start the table managers for the index tree
        self.node_class = node_class
        self.index_name = index_name
        self.btree_table_manager = TableManager(BTree, self.get_manager_name())
        self.btree_node_table_manager = TableManager(node_class, self.get_node_manager_name())
        self.root = None

        # Load root if exists
        if self.get_root_id():
            self.get_root_node()
        else:
            self.create_root()

    # Return a unique name for this index with it's key type
    def get_manager_name(self):
        return self.index_name + FileName.INDEX_SEPARATOR + self.node_class.get_node_type() + FileName.INDEX_MANAGER

    # Return a unique name for this index node with it's key type
    def get_node_manager_name(self):
        return self.index_name + FileName.INDEX_SEPARATOR + self.node_class.get_node_type() + FileName.INDEX_DATA

    # Get the saved root id in the database if exists
    # Return TRUE for success and FALSE if root is None
    def get_root_id(self) -> bool:
        saved_self = self.btree_table_manager.find_by_id(0)
        if not saved_self:
            return False
        else:
            self.root_id = saved_self.root_id
            return True

    # Load the root node from node table
    def get_root_node(self):
        self.root = self.btree_node_table_manager.find_by_id(self.root_id)

    # Add a root if not exists
    def create_root(self):
        # Create a instance with proper type
        new_root = self.node_class()
        # Save in database
        new_root = self.btree_node_table_manager.save(new_root)
        # Update the class data with database info
        self.root_id = new_root.id
        self.root = new_root

    # Return the id of the object with the key
    def search(self, key) -> int:
        node = self.root

        position = 0

        # Try to find the key in the BTree using the nodes
        # If key found return the id referenced by the key
        # Else return None
        while True:
            # Find the first key greater than or equal to key
            while position < len(node.keys) and key > node.keys[position]:
                i = i + 1

            if node.keys[i] == key:
                return node.content[i]

            if node.leaf:
                return None

            node = self.get_node_by_id(node.children_id)

    def get_node_by_id(self, node_id: int) -> object:
        return self.btree_node_table_manager.find_by_id(node_id)

    def insert(self, key, content):
        # If root is full, then tree grows in height
        if len(key) == _KEYS_VALUES_ARRAY_SIZE * 2:
            # Create a new node
            new_node = self.node_class()
            new_node.leaf = False
            # Make the old root a child of new root
            new_node.children_id.append(self.root_id)
            # Split the old root and move 1 key to the new root
            self.split_child(0, self.root)
            # New root has two children now.
            # Decide which of the two children is going to have new key
            i = 0
            if new_node.keys[0] < key:
                i = i + 1

            self.insert_non_full(new_node, key)

            # Save the new node on database
            self.btree_node_table_manager.save(new_node)

            # Update the root
            self.root = new_node
            self.root_id = new_node.id
        else:
            self.insert_non_full(self.root, key)


    def split_child(self):
        return None
