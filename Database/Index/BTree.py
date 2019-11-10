from Database.Cons import SupportedTypes


class BTreeNode:
    id = 0
    keys = []
    keys_size = 1000
    min_degree = 0
    child_ids = []
    child_ids_size = 1000   # PROBLEM BECAUSE THE NODE CHILD IDS IS LIMITED
    child_ids_type = SupportedTypes.INT_SIZE
    n_keys = 0
    leaf = True

    def __init__(self, min_degree):
        self.min_degree = 2 * min_degree - 1
        self.n_keys = 0

    def get_child_by_id(self, child_id: int) -> object:
        return

    def transverse(self):
        x = 0

        for x in range(0, self.n_keys):
            if not self.leaf:
                child = self.get_child_by_id(self.child_ids[x])
                child.transverse()

        if not self.leaf:
            child = self.get_child_by_id(self.child_ids[x])
            child.transverse()

    def search(self, k: int):
        i = 0
        while i < self.n_keys and k > self.keys[i]:
            i = i + 1

        if self.keys[i] == k:
            return self

        if self.leaf:
            return None

        child = self.get_child_by_id(self.child_ids[i])

        return child.search(k)


class BTreeIntNode(BTreeNode):
    keys_type = SupportedTypes.INT_NAME

    n_keys = 0
    leaf = True


class BTree:
    root_id = 0
    min_degree = 0
