import math

from Database.Error import BTreeError
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

        # Load root if exists, if not create one
        if not self._get_btree_info():
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
        root = self.btree_node_table_manager.find_by_id(self.b)

        # Verify if the tree is empty
        if len(root.keys) != 0:
            self._insert_non_empty_node(key, content)
        else:
            self._insert_empty_node(root, key, content)

    # Delete the key and it's content from BTree
    # Return True in success and False if key doesn't exists
    def delete(self, key) -> bool:
        # Get the root node
        root = self._get_root()

        # Verify if the tree is empty
        if len(root.keys) != 0:
            return self._delete_by_key(key)
        else:
            return False

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

            if len(parent_node.keys) > parent_node.keys_size:
                # Continue with the split
                self._split_node(parent_node)
            else:
                self.btree_node_table_manager.save(parent_node)
        else:  # There no is parent node, it's the root
            root = self._get_root()
            root.keys = [key]
            root.contents = [content]
            root.children_ids = [left_node.id, right_node.id]
            # Update in database
            self.btree_node_table_manager.save(root)

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
            if self._is_full(child):
                # If the child is full, then split it
                self.split_child(i + 1, node, child)

                # After split, the middle key of children_id[i] goes up and
                # children_id[i] is splitted into two.  See which of the tw
                # is going to have the new key
                if node.keys[i + 1] < key:
                    i = i + 1

            self._insert_non_full(child, key)

    ####################################################################################################################
    # BTree delete aux function
    # See a tutorial in:
    # https://medium.com/@vijinimallawaarachchi/all-you-need-to-know-about-deleting-keys-from-b-trees-9090f3334b5c

    # Find the node of the key and delete respecting BTree rules
    # Return True if the key exists and False if not
    def _delete_by_key(self, key) -> bool:
        node, position, found = self._search(key)

        # Just insert not existent keys
        if found:
            self._delete_key_from_node_by_position(node, position)
            return True
        else:  # If found update the content value
            return False

    # Delete a key and it's content of a node using the given node and position
    def _delete_key_from_node_by_position(self, node, position):
        # Case 1: Node is leaf
        if self._is_leaf(node):
            if not self._has_minimum_size(node):
                # Case 1.a: node is a leaf and has more keys than the min
                # Just remove the element and save
                self._delete_key_in_node_and_save(node, position)
            else:
                parent = self._get_parent(node)
                # Case 1.b: node is a leaf and has the min numbers of keys
                if not self._borrow_from_sibling_and_delete(node, position, parent):
                    self._merge_nodes_and_delete(node, position, parent, True)
                    # Check if parent has the min. size
                    while parent is not None and not self._greater_or_equal_than_minimum_size(parent):
                        grandparent = self._get_parent(parent)
                        self._merge_nodes_and_delete(parent, 0, grandparent, False)
                        parent = grandparent
        else:  # Case 2: Node is intern or root
            predecessor = self._get_predecessor_child(node, position)
            if predecessor is not None:
                # Case 2.a: Has predecessor child, get it's biggest element
                self._borrow_from_predecessor_and_delete(node, position, predecessor)
                # Check if parent has the min. size
                while predecessor is not None and not self._greater_or_equal_than_minimum_size(predecessor):
                    parent = self._get_parent(predecessor)
                    self._merge_nodes_and_delete(predecessor, 0, parent, False)
                    predecessor = parent
            else:
                # Case 2.b: Has only a child that precedes, get it's smallest element
                successor = self._get_successor_child(node, position)

                if successor is not None:
                    self._borrow_from_successor_and_delete(node, position, successor)
                else:
                    # Case 2.c: The nodes that precedes and follow the current target has min. size
                    self._merge_nodes_borrow_and_delete(node, position, predecessor, successor)

    # Case 2.a: Get the biggest key of a node and put in the parent, deleting the required key
    def _borrow_from_predecessor_and_delete(self, node, position, predecessor):
        # Remove the key and insert the predecessor key
        node.keys[position] = predecessor.keys.pop()
        node.contents[position] = predecessor.contents.pop()

        # Save the results
        self.btree_node_table_manager.save(predecessor)
        self.btree_node_table_manager.save(node)

    # Case 2.b: Get the smallest key of a node and put in the parent, deleting the required key
    def _borrow_from_successor_and_delete(self, node, position, successor):
        # Remove the key and insert the predecessor key
        node.keys[position] = successor.keys.pop()
        node.contents[position] = successor.contents.pop()

        # Save the results
        self.btree_node_table_manager.save(successor)
        self.btree_node_table_manager.save(node)

    # Case 2.c: Predecessor and node which precedes haven't size to borrow
    def _merge_nodes_borrow_and_delete(self, node, position, predecessor, successor):
        # Merge the successor and predecessor
        predecessor.keys.append(successor.keys)
        predecessor.contents.append(successor.contents)

        # Remove the key in the node
        del node.keys[position]
        del node.contents[position]
        # Delete the children_id of the successor
        del node.children_ids[position + 1]

        # Delete the successor
        self.btree_node_table_manager.delete(successor)

        # Save the results
        self.btree_node_table_manager.save(predecessor)
        self.btree_node_table_manager.save(node)

    # Case 1.b.b: Merge the node and a sibling to remove the element
    def _merge_nodes_and_delete(self, node, position, parent, delete):
        # Verify if the node is root
        if self._is_root(node):
            # Transfer the child data for the root
            child = self._get_node_by_id(node.children_ids[0])
            node.keys = child.keys
            node.contents = child.contents
            node.children_ids = child.children_ids

            self._update_children_id(node)

            self.btree_node_table_manager.save(node)
            self.btree_node_table_manager.delete(child)

            return

        # Try left sibling first
        if not self._merge_with_left_sibling_and_delete(node, position, parent, delete):
            self._merge_with_right_sibling_and_delete(node, position, parent, delete)

    # Try merge node with left sibling and delete the key
    # Return True if the left node exists and everything was done or False if the left node not exists
    def _merge_with_left_sibling_and_delete(self, node, position, parent, delete) -> bool:
        # Get left sibling
        sibling = self._get_left_sibling(node, parent)

        # If not exists return False
        if sibling is None:
            return False
        # Else continue with the merge process

        # Get the position of the sibling node in the parent
        sibling_position = parent.children_ids.index(sibling.id)

        if delete:
            # Remove the key from node
            del node.keys[position]
            del node.contents[position]

        # Get the key from parent and insert in the left sibling
        sibling.keys.append(parent.keys.pop(sibling_position))
        sibling.contents.append(parent.contents.pop(sibling_position))

        # Merge nodes
        sibling.keys.extend(node.keys)
        sibling.contents.extend(node.contents)

        # Remove the id of the node in the parent children_ids
        del parent.children_ids[sibling_position + 1]

        # Remove node from database
        self.btree_node_table_manager.delete(node)

        # Save sibling and parent
        self.btree_node_table_manager.save(sibling)
        self.btree_node_table_manager.save(parent)

        return True

    # Try merge node with right sibling and delete the key
    # Return True if the right node exists and everything was done or False if the right node not exists
    def _merge_with_right_sibling_and_delete(self, node, position, parent, delete) -> bool:
        # Get left sibling
        sibling = self._get_right_sibling(node, parent)

        # If not exists return False
        if sibling is None:
            return False
        # Else continue with the merge process

        # Get the position of the sibling node in the parent
        node_position = parent.children_ids.index(node.id)

        if delete:
            # Remove the key from node
            del node.keys[position]
            del node.contents[position]

        # Get the key from parent and insert in the node
        node.keys.append(parent.keys.pop(node_position))
        node.contents.append(parent.contents.pop(node_position))

        # Merge nodes
        node.keys.extend(sibling.keys)
        node.contents.extend(sibling.contents)
        node.children_ids.extend(sibling.children_ids)
        self._update_children_id(node)

        # Remove the id of the sibling in the parent children_ids
        del parent.children_ids[node_position + 1]

        # Remove sibling from database
        self.btree_node_table_manager.delete(sibling)

        # Save node and parent
        self.btree_node_table_manager.save(node)
        self.btree_node_table_manager.save(parent)

    # Case 1.b.a: Try to borrow from a sibling to delete a value respecting the BTree rules
    # Return True if success and False if siblings can't borrow
    def _borrow_from_sibling_and_delete(self, node, position, parent) -> bool:
        # Try left sibling first
        l_sibling = self._get_left_sibling(node, parent)

        if l_sibling is not None and not self._has_minimum_size(l_sibling):
            self._borrow_from_left_sibling_and_delete(self, node, position, parent, l_sibling)
        else:
            r_sibling = self._get_right_sibling(node, parent)

            if r_sibling is not None and not self._has_minimum_size(r_sibling):
                self._borrow_from_right_sibling_and_delete(self, node, position, parent, r_sibling)
            else:
                return False

        return True

    # Borrow and rotate with left sibling
    def _borrow_from_left_sibling_and_delete(self, node, position, parent, sibling):
        parent_position = parent.children_ids.index(node.id)

        # Remove the key and insert parent values
        del node.keys[position]
        del node.contents[position]
        node.keys.insert(0, parent.keys[parent_position - 1])
        node.contents.insert(0, parent.contents[parent_position - 1])

        # Remove value from sibling and put in parent
        parent.keys[parent_position - 1] = sibling.keys.pop()
        parent.contents[parent_position - 1] = sibling.contents.pop()

        # Save everything
        self.btree_node_table_manager.save(sibling)
        self.btree_node_table_manager.save(parent)
        self.btree_node_table_manager.save(node)

    # Borrow and rotate with right sibling
    def _borrow_from_right_sibling_and_delete(self, node, position, parent, sibling):
        parent_position = parent.children_ids.index(node.id)

        # Remove the key and insert parent values
        del node.keys[position]
        del node.contents[position]
        node.keys.append(parent.keys[parent_position])
        node.contents.append(parent.contents[parent_position])

        # Remove value from sibling and put in parent
        parent.keys[parent_position] = sibling.keys.pop(0)
        parent.contents[parent_position] = sibling.contents.pop(0)

        # Save everything
        self.btree_node_table_manager.save(sibling)
        self.btree_node_table_manager.save(parent)
        self.btree_node_table_manager.save(node)

    # Only remove the key and it's content and save
    def _delete_key_in_node_and_save(self, node, position):
        del node.keys[position]
        del node.contents[position]
        self.btree_node_table_manager.save(node)

    # Only insert the key and it's content in a position and save
    def _insert_key_in_node_and_save(self, node, position, key, content):
        node.keys = node.keys[:position] + [key] + node.content[position:]
        node.contents = node.contents[:position] + [content] + node.contents[position:]
        self.btree_node_table_manager.save(node)

    # Return the immediate right sibling of a node
    def _get_right_sibling(self, node, parent):
        position = parent.children_ids.index(node.id)

        # Return if exists
        if len(parent.children_ids) > position + 1:
            return self._get_node_by_id(parent.children_ids[position + 1])

        # Return None if not exists
        return None

    # Return the immediate left sibling of a node
    def _get_left_sibling(self, node, parent):
        position = parent.children_ids.index(node.id)

        # Return if exists
        if position - 1 >= 0:
            return self._get_node_by_id(parent.children_ids[position - 1])

        # Return None if not exists
        return None

    # Return the child before a node item using it's position
    def _get_predecessor_child(self, node, position):
        if len(node.children_ids) > position >= 0:
            predecessor = self._get_node_by_id(node.children_ids[position])
        else:
            return None

        if predecessor is None:
            return None

        while not self._is_leaf(predecessor):
            biggest_child_id = predecessor.children_ids[len(predecessor.children_ids) - 1]
            predecessor = self._get_node_by_id(biggest_child_id)

        return predecessor

    # Return the child after a node item using it's position
    def _get_successor_child(self, node, position):
        if len(node.children_ids) >= position + 1:
            successor = self._get_node_by_id(node.children_ids[position + 1])
        else:
            return None

        if successor is None:
            return None

        while not self._is_leaf(predecessor):
            smallest_child_id = predecessor.children_ids[0]
            predecessor = self._get_node_by_id(smallest_child_id)

        return predecessor

    # Return the parent of a node
    def _get_parent(self, node):
        return self._get_node_by_id(node.parent_id)

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
    def _is_root(node) -> bool:
        return node.parent_id == -1

    # Return True if a node is full
    @staticmethod
    def _is_full(node) -> bool:
        return len(node.keys) == node.keys_size

    # Return True if a node has the minimum size allowed
    @staticmethod
    def _has_minimum_size(node) -> bool:
        return len(node.keys) == math.floor(node.keys_size/2)

    # Return True if a node has a size equal or greater than the minimum allower
    @staticmethod
    def _greater_or_equal_than_minimum_size(node) -> bool:
        return len(node.keys) >= math.floor(node.keys_size/2)

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

    # Return the root
    def _get_root(self):
        return self.btree_node_table_manager.find_by_id(self.btree_info.root_id)

    ####################################################################################################################
