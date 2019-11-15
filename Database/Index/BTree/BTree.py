from Database.Index.BTree import BTreeCons
from Database.Index.BTree.BTreeInfo import BTreeInfo
from Database.TableManager import TableManager
from Database.Cons import FileName
import Database.Helpers.ListHelper as ListHelper


class BTree:
    def __init__(self, index_name: str, node_class: object, ref_class: object):
        # Start the table managers for the index tree
        self.node_class = node_class
        self.index_name = index_name
        self.btree_info = BTreeInfo()
        self.btree_info_table_manager = TableManager(
            BTreeInfo, self._get_index_dir(index_name), self._get_manager_name(), ref_class)
        self.btree_node_table_manager = TableManager(
            node_class, self._get_index_dir(index_name), self._get_node_manager_name(), ref_class)

        # Load root if exists
        if self._get_btree_info():
            self._get_root_node()
        else:
            self._create_root()

    # Return the id of the object with the key
    def search(self, key) -> int:
        node, position, found = self._search(key)

        # If find return the content
        if found:
            return node.contents[position]
        else:  # If not return None
            return None

    # Insert and update a key with it's content
    def insert(self, key, content):
        # Get the root node
        root = self.btree_info.root

        # Verify if the tree is empty
        if len(root.keys) != 0:
            self._insert_non_empty_node(key, content)
        else:
            self._insert_empty_node(root, key, content)

    # Drop all index data
    def drop(self):
        self.btree_info_table_manager.drop()

    ####################################################################################################################
    # BTree insert aux functions

    # Insert when the node is not empty
    def _insert_non_empty_node(self, key, content):
        node, position, found = self._search(key)

        # Just insert not existent keys
        if not found:
            self._insert_leaf_node(node, key, content)
        else:  # If found update the content value
            node.contents[position] = content
            self.btree_node_table_manager.save(node)

    # Split the node and insert in the right position
    def _split_node(self, node):
        parent_node = self._get_node_by_id(node.parent_id)

        # Get the middle position to split
        middle = ListHelper.find_middle_position(node.keys)

        # Create a new left node
        left_node = self.node_class()
        left_node.keys = node.keys[:middle]
        left_node.contents = node.contents[:middle]
        left_node.children_ids = node.children_ids[:middle + 1]
        # Utilize the node if parent_node exists
        if parent_node:
            left_node.id = node.id
            left_node.saved = node.saved
            left_node.parent_id = node.parent_id
            # Remove to add in the right order after
            parent_node.children_ids.remove(node.id)
        else:
            left_node.parent_id = node.id
        # Save in database
        self.btree_node_table_manager.save(left_node)

        # Update the children
        self._update_children_id(left_node)

        # Create a new right node
        right_node = self.node_class()
        right_node.keys = node.keys[middle + 1:]
        right_node.contents = node.contents[middle + 1:]
        right_node.children_ids = node.children_ids[middle + 1:]
        if parent_node:
            right_node.parent_id = node.parent_id
        else:
            right_node.parent_id = node.id
        # Save in database
        self.btree_node_table_manager.save(right_node)

        # Update the children
        self._update_children_id(right_node)

        # Update the parent node
        key = node.keys[middle]
        content = node.contents[middle]

        if parent_node:
            position = self._get_insert_position(parent_node, key)
            # Add the key and the content in the right position in the node lists
            parent_node.keys = parent_node.keys[:position] + [key] \
                               + parent_node.keys[position:]
            parent_node.contents = parent_node.contents[:position] + [content] \
                                   + parent_node.contents[position:]
            parent_node.children_ids = parent_node.children_ids[:position] + [left_node.id, right_node.id] \
                                       + parent_node.children_ids[position:]

            if self._is_root(parent_node):
                self.btree_info.root = parent_node
                self.btree_info.root_id = parent_node.id

            if len(parent_node.keys) > parent_node.keys_size:
                # Continue with the split
                self._split_node(parent_node)
            else:
                self.btree_node_table_manager.save(parent_node)
        else:  # There no is parent node, it's the root
            self.btree_info.root.keys = [key]
            self.btree_info.root.contents = [content]
            self.btree_info.root.children_ids = [left_node.id, right_node.id]
            # Update in database
            self.btree_node_table_manager.save(self.btree_info.root)

    # Insert a new value in a leaf
    def _insert_leaf_node(self, node, key, content):
        self._insert_key_in_leaf(node, key, content)
        # Verify if the node has more keys than the degree less one
        if len(node.keys) > node.keys_size:
            self._split_node(node)
        else:
            # Save the updated node
            self.btree_node_table_manager.save(node)

    # Insert a key in a leaf node
    def _insert_key_in_leaf(self, node, key, content):
        position = self._get_insert_position(node, key)

        # Add the key and the content in the right position in the node lists
        node.keys = node.keys[0:position] + [key] + node.keys[position:len(node.keys)]
        node.contents = node.contents[0:position] + [content] + node.contents[position:len(node.contents)]

    # Update the children's parent_id of a node
    def _update_children_id(self, node):
        for child_id in node.children_ids:
            child_node = self._get_node_by_id(child_id)
            child_node.parent_id = node.id
            self.btree_node_table_manager.save(child_node)

    @staticmethod
    def _get_insert_position(node, key) -> int:
        count = 0
        while count < len(node.keys) and key > node.keys[count]:
            count = count + 1

        return count

    # Insert in the base case, when the node is empty
    def _insert_empty_node(self, node, key, content):
        node.keys.append(key)
        node.contents.append(content)
        self.btree_node_table_manager.save(node)

    def _insert_non_full(self, node, key):
        # Initialize index as index of rightmost element
        i = len(node.keys) - 1

        # If this is a leaf node
        if self._is_leaf(node):
            # The following loop does two things
            # a) Finds the location of new key to be inserted
            # b) Moves all greater keys to one place ahead
            while i >= 0 and node.keys[i] > key:
                node.keys[i + 1] = node.keys[i]
                i = i - 1

            # Insert the new key at found location
            node.keys[i + 1] = key
        else:  # If this node is not leaf
            # Find the child which is going to have the new key
            while i >= 0 and node.keys[i] > key:
                i = i - 1

            # See if the found child is full
            child = self._get_node_by_id(node.children[i + 1])
            if len(child.keys) == BTreeInfo.KEYS_VALUES_ARRAY_SIZE * 2 - 1:
                # If the child is full, then split it
                self.split_child(i + 1, node, child)

                # After split, the middle key of children_id[i] goes up and
                # children_id[i] is splitted into two.  See which of the tw
                # is going to have the new key
                if node.keys[i + 1] < key:
                    i = i + 1

            self._insert_non_full(child, key)

    ####################################################################################################################
    ####################################################################################################################
    # BTree internal functions

    # Search for the key
    # If find: return the node, the position of the content and true
    # If not: return the last node, none and false
    def _search(self, key) -> (object, int, bool):
        node = self.btree_info.root
        position = 0

        # Try to find the key in the BTree using the nodes
        # If key found return the id referenced by the key
        # Else return None
        while True:
            # Find the first key smaller or equal than key
            while position < len(node.keys) and key > node.keys[position]:
                position = position + 1

            # Verify if the key found is equal
            # If true return the content of this key
            if position < len(node.keys) and node.keys[position] == key:
                return node, position, True

            # Verify if the node is a leaf, if true the search ends without find the key
            if self._is_leaf(node):
                return node, None, False

            # Continue the search in the child
            node = self._get_node_by_id(node.children_ids[position])
            position = 0

    # Get the saved root id in the database if exists
    # Return TRUE for success and FALSE if root is None
    def _get_btree_info(self) -> bool:
        btree_info = self.btree_info_table_manager.find_by_id(0)

        if not btree_info:
            return False
        else:
            return True

    # Load the root node from node table
    def _get_root_node(self):
        self.btree_info.root = self.btree_node_table_manager.find_by_id(self.btree_info.root_id)

    # Add a root if not exists
    def _create_root(self):
        # Create a instance with proper type
        new_root = self.node_class()
        # Save in database
        self.btree_node_table_manager.save(new_root)
        # Update the class data with database info
        self.btree_info = BTreeInfo()
        self.btree_info.root_id = new_root.id
        self.btree_info.root = new_root
        # Save main in the database
        self.btree_info_table_manager.save(self.btree_info)

    def _get_node_by_id(self, node_id: int) -> object:
        return self.btree_node_table_manager.find_by_id(node_id)

    @staticmethod
    def _is_leaf(node):
        return len(node.children_ids) == 0

    # Return True if the node is the root
    @staticmethod
    def _is_root(node):
        return node.parent_id == -1

    ####################################################################################################################
    ####################################################################################################################
    # Dir internal manager

    # Return the dir of the index
    def _get_index_dir(self, index_name: str):
        return index_name + FileName.INDEX_SEPARATOR + self.node_class.get_node_type()

    # Return a unique name for this index with it's key type
    @staticmethod
    def _get_manager_name():
        return FileName.INDEX_MANAGER

    # Return a unique name for this index node with it's key type
    @staticmethod
    def _get_node_manager_name():
        return FileName.INDEX_DATA

    ####################################################################################################################

